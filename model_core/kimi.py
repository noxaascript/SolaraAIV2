from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_ID = "moonshotai/Kimi-K2.7-Code"


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_ID,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)


def run_kimi(prompt):

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)


    with torch.no_grad():

        output = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True
        )


    return tokenizer.decode(
        output[0],
        skip_special_tokens=True
    )
