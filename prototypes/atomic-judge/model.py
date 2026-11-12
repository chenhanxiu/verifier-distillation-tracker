"""Causal backbone + LoRA + shared three-class readout; no text generation."""
import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer
from peft import LoraConfig, PeftModel, get_peft_model
from data import encode, LABELS


class Judge(nn.Module):
    def __init__(self, backbone):
        super().__init__()
        self.backbone = backbone
        self.head = nn.Linear(backbone.config.hidden_size, len(LABELS))

    def forward(self, input_ids, attention_mask, positions):
        h = self.backbone(input_ids=input_ids, attention_mask=attention_mask,
                          use_cache=False, return_dict=True).last_hidden_state
        selected = h[torch.arange(h.shape[0], device=h.device)[:,None], positions.clamp_min(0)]
        return self.head(selected.to(self.head.weight.dtype))


def build(base, checkpoint=None, rank=8, dtype='float32'):
    tokenizer = AutoTokenizer.from_pretrained(str(checkpoint) if checkpoint else base, local_files_only=True)
    tokenizer.padding_side = 'right'
    if tokenizer.pad_token_id is None:
        if tokenizer.eos_token_id is None:
            raise ValueError('Tokenizer needs a pad or eos token')
        tokenizer.pad_token = tokenizer.eos_token
    backbone = AutoModel.from_pretrained(base, local_files_only=True,
                                         torch_dtype=getattr(torch, dtype))
    if getattr(backbone.config, 'is_encoder_decoder', False) or not hasattr(backbone.config, 'hidden_size'):
        raise ValueError('Use a decoder-only backbone with hidden_size')
    if checkpoint:
        backbone = PeftModel.from_pretrained(backbone, str(checkpoint / 'adapter'))
    else:
        backbone = get_peft_model(backbone, LoraConfig(r=rank, lora_alpha=2*rank,
                    lora_dropout=0.05, target_modules='all-linear', bias='none'))
    judge = Judge(backbone)
    if checkpoint:
        judge.head.load_state_dict(torch.load(checkpoint/'head.pt', map_location='cpu', weights_only=True))
    return judge, tokenizer


def collate(tokenizer, records, max_length, device):
    encoded = [encode(tokenizer, rs, max_length) for rs in records]
    length = max(len(ids) for ids,_ in encoded)
    width = max(len(pos) for _,pos in encoded)
    ids = torch.full((len(records),length), tokenizer.pad_token_id, dtype=torch.long)
    mask = torch.zeros_like(ids)
    positions = torch.full((len(records),width), -1, dtype=torch.long)
    labels = torch.full_like(positions, -100)
    for b, ((tokens,pos),rows) in enumerate(zip(encoded,records)):
        ids[b,:len(tokens)] = torch.tensor(tokens)
        mask[b,:len(tokens)] = 1
        positions[b,:len(pos)] = torch.tensor(pos)
        labels[b,:len(rows)] = torch.tensor([LABELS.index(r['label']) if r.get('label') in LABELS else -100 for r in rows])
    return ({'input_ids':ids.to(device), 'attention_mask':mask.to(device),
             'positions':positions.to(device)}, labels.to(device))
