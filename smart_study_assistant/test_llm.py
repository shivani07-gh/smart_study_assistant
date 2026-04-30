from openai import OpenAI

client = OpenAI(
  api_key="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",
  base_url="https://integrate.api.nvidia.com/v1"
)

response = client.embeddings.create(
    input=["What is the capital of France?"],
    model="nvidia/llama-3.2-nemoretriever-300m-embed-v1",
    encoding_format="float",
    extra_body={"input_type": "query", "truncate": "NONE"}
)

print(response.data[0].embedding)
