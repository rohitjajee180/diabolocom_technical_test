// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview
client<llm> Llama_405b {
  provider openai-generic
  options {
    base_url "https://api.studio.nebius.com/v1/"
    model "meta-llama/Meta-Llama-3.1-405B-Instruct"
    temperature 0.0
    api_key env.NE_API_KEY
  }
}