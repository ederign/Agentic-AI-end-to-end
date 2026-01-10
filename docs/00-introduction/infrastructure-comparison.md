# LLM Infrastructure Layer Comparison

> **Note:** Research compiled during collaborative exploration with Claude (Anthropic).

## Infrastructure Layer Categories

There are **different types** of infrastructure layers in the LLM ecosystem:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your Application                              │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│              API Gateway / Proxy Layer                           │
│   LiteLLM │ Portkey │ OpenRouter │ LlamaStack │ Helicone        │
│   (unified API, routing, fallback, observability)               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│              Inference Engine Layer                              │
│   vLLM │ TGI │ Ollama │ llama.cpp │ TensorRT-LLM                │
│   (actually runs the models on GPU/CPU)                         │
└─────────────────────────────────────────────────────────────────┘
```

## Gateway/Proxy Layer Comparison

| Tool | Open Source | Self-Host | Models | Key Differentiator |
|------|-------------|-----------|--------|-------------------|
| **LlamaStack** | Yes | Yes | Via providers | Full stack (inference, agents, RAG, safety, evals) |
| **LiteLLM** | Yes | Yes | 100+ | Lightweight, universal proxy |
| **Portkey** | Yes | Paid ($49+/mo) | 1600+ | Enterprise controls, routing |
| **OpenRouter** | No | No | 300+ | Zero setup, 5% markup |
| **Helicone** | Yes | Yes | Via proxy | Strong analytics/observability |

## Inference Engine Layer Comparison

| Tool | Focus | Best For |
|------|-------|----------|
| **vLLM** | High throughput GPU serving | Production, high-traffic |
| **Ollama** | Easy local setup | Development, prototyping |
| **TGI** | HuggingFace ecosystem | HF model deployment |
| **llama.cpp** | CPU inference, edge | Low-resource environments |
| **TensorRT-LLM** | NVIDIA optimization | Maximum GPU performance |

## LlamaStack's Unique Position

LlamaStack is **more than a gateway** - it's a full application platform:

| Feature | LiteLLM | Portkey | LlamaStack |
|---------|---------|---------|------------|
| API routing | ✅ | ✅ | ✅ |
| Unified interface | ✅ | ✅ | ✅ |
| Fallback/retry | ✅ | ✅ | ✅ |
| Cost tracking | ✅ | ✅ | ✅ |
| **Responses API** | ❌ | ❌ | ✅ |
| **Agents API** | ❌ | ❌ | ✅ |
| **Vector stores** | ❌ | ❌ | ✅ |
| **File management** | ❌ | ❌ | ✅ |
| **Safety shields** | ❌ | ❌ | ✅ |
| **Evaluations** | ❌ | ❌ | ✅ |

### Key Insight

LlamaStack isn't just competing with LiteLLM/Portkey - it's a **superset** that includes gateway features PLUS application-level features (agents, RAG, safety).

## When to Use What

| Scenario | Recommendation |
|----------|----------------|
| Just need multi-provider routing | **LiteLLM** (simpler, lighter) |
| Need observability + routing | **Portkey** or **Helicone** |
| Zero infrastructure, quick start | **OpenRouter** (managed) |
| Full agentic platform + model freedom | **LlamaStack** |
| Running your own models locally | **vLLM** + gateway of choice |
| Development/prototyping | **Ollama** (easiest setup) |

## Typical Production Stacks

### Minimal Stack
```
App → LiteLLM → OpenAI/Anthropic/etc.
```

### Self-Hosted Stack
```
App → LiteLLM → vLLM (your models)
```

### Full Agentic Stack
```
App → LlamaStack → vLLM/OpenAI/Ollama
         │
         ├── Inference API
         ├── Responses API (agents)
         ├── Vector IO (RAG)
         └── Safety shields
```

### Enterprise Stack
```
App → Portkey → Multiple providers
         │
         ├── Smart routing
         ├── Cost optimization
         ├── Compliance logging
         └── Fallback chains
```

## LlamaStack + Inference Engines

LlamaStack can use various inference engines as providers:

```yaml
providers:
  inference:
    # Option 1: Cloud provider
    - provider_type: remote::openai

    # Option 2: Self-hosted vLLM
    - provider_type: remote::vllm
      config:
        url: http://vllm-server:8000/v1

    # Option 3: Local Ollama
    - provider_type: remote::ollama
      config:
        url: http://localhost:11434
```

## Sources

- [Top 5 LLM Gateways in 2025 - Helicone](https://www.helicone.ai/blog/top-llm-gateways-comparison-2025)
- [6 Best LLM Gateways in 2025 - TrueFoundry](https://www.truefoundry.com/blog/best-llm-gateways)
- [LiteLLM Alternatives - Pomerium](https://www.pomerium.com/blog/litellm-alternatives)
- [vLLM or llama.cpp - Red Hat Developer](https://developers.redhat.com/articles/2025/09/30/vllm-or-llamacpp-choosing-right-llm-inference-engine-your-use-case)
- [Local LLM Hosting Guide 2025](https://www.glukhov.org/post/2025/11/hosting-llms-ollama-localai-jan-lmstudio-vllm-comparison/)
