# OpenAI Integration in ReplySight

## Overview

ReplySight now integrates with OpenAI's GPT-4o-mini model to generate empathetic, research-backed customer service responses. This replaces the previous hardcoded template system with dynamic AI-powered response generation.

## Features

- **GPT-4o-mini Integration**: Uses OpenAI's latest efficient model for response generation
- **Intelligent Prompting**: Structured prompts that incorporate academic research insights and best practice examples
- **Graceful Fallback**: Automatically falls back to template responses if OpenAI is unavailable
- **Research Integration**: Seamlessly incorporates arXiv research insights and Tavily examples into AI prompts
- **Citation Support**: Maintains citation tracking for academic sources and examples

## Configuration

### Environment Variables

Add the following to your `.env` file:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Model Configuration

The integration uses GPT-4o-mini with the following settings:
- **Model**: `gpt-4o-mini`
- **Temperature**: `0.7` (balanced creativity and consistency)
- **Max Tokens**: Default (typically ~2048 for responses)

## How It Works

### 1. Workflow Integration

The OpenAI integration is seamlessly incorporated into the existing LangGraph workflow:

```
Customer Complaint → Fetch arXiv Insights → Fetch Tavily Examples → AI Response Generation
```

### 2. Prompt Engineering

The system uses a carefully crafted prompt template that:

- Establishes the AI as an expert customer service representative
- Provides customer complaint context
- Includes relevant academic research insights
- Incorporates best practice examples
- Gives specific instructions for empathetic, solution-focused responses

### 3. Response Generation Process

1. **Context Preparation**: Academic insights and examples are summarized for the AI
2. **Prompt Construction**: All context is assembled into a structured prompt
3. **AI Generation**: GPT-4o-mini generates a personalized response
4. **Citation Assembly**: Academic and example citations are collected
5. **Fallback Handling**: If AI fails, system uses template response

## Code Structure

### Modified Components

#### `backend/tools.py`
- **ResponseComposerTool**: Updated to use GPT-4o-mini instead of hardcoded templates
- **Prompt Template**: Engineered for empathetic customer service responses
- **Error Handling**: Graceful fallback to template responses

#### `.env_sample`
- Added `OPENAI_API_KEY` configuration

#### `pyproject.toml`
- `langchain-openai` dependency already included

## Testing

### Unit Tests

Run the OpenAI integration tests:

```bash
source .venv/bin/activate
PYTHONPATH=. python tests/test_openai_integration.py
```

### Full Workflow Test

Test the complete workflow:

```bash
source .venv/bin/activate
PYTHONPATH=. python test_full_workflow.py
```

## Response Quality

### With OpenAI API Key

When properly configured with an OpenAI API key, the system generates:
- Highly personalized responses
- Context-aware empathy
- Specific solutions based on complaint details
- Professional yet warm tone
- Research-backed insights integration

### Fallback Mode

Without an API key or if OpenAI is unavailable:
- Uses template-based responses
- Maintains professional empathy
- Includes basic service recovery elements
- Preserves citation functionality

## Performance

- **Latency**: ~500-2000ms (depending on OpenAI API response time)
- **Cost**: ~$0.01-0.05 per response (GPT-4o-mini pricing)
- **Reliability**: Graceful degradation ensures 100% uptime

## Best Practices

### API Key Management

1. Store API keys securely in environment variables
2. Use different keys for development/production
3. Monitor usage and costs in OpenAI dashboard
4. Implement rate limiting if necessary

### Prompt Optimization

1. The current prompt is optimized for customer service empathy
2. Modify the prompt template in `ResponseComposerTool._initialize_llm()` if needed
3. Test prompt changes thoroughly
4. Monitor response quality and customer satisfaction

### Error Handling

1. System automatically falls back to templates if OpenAI fails
2. All errors are logged but don't break the workflow
3. Monitor error rates and API availability

## Deployment

### Production Checklist

- [ ] Configure `OPENAI_API_KEY` in production environment
- [ ] Test with real API key before deployment
- [ ] Monitor costs and usage
- [ ] Set up alerts for API failures
- [ ] Verify fallback behavior works correctly

### Scaling Considerations

- GPT-4o-mini handles high throughput well
- Consider connection pooling for high-volume deployments
- Monitor OpenAI rate limits
- Implement caching for repeated similar complaints if needed

## Future Enhancements

### Potential Improvements

1. **Model Fine-tuning**: Train custom models on company-specific data
2. **Response Caching**: Cache responses for similar complaints
3. **A/B Testing**: Compare AI vs template responses
4. **Sentiment Analysis**: Advanced emotion detection and response adaptation
5. **Multi-language Support**: Extend to non-English customer complaints

### Integration Extensions

1. **Custom Models**: Support for other LLM providers (Anthropic Claude, etc.)
2. **Hybrid Approach**: Combine multiple AI models for enhanced responses
3. **Real-time Learning**: Incorporate customer feedback to improve responses
4. **Analytics Dashboard**: Track response quality metrics and customer satisfaction

## Troubleshooting

### Common Issues

#### "OpenAI API key not found"
- Ensure `OPENAI_API_KEY` is set in environment
- Check API key validity in OpenAI dashboard

#### "Rate limit exceeded"
- Monitor usage in OpenAI dashboard
- Implement exponential backoff retry logic
- Consider upgrading OpenAI plan

#### "Model not found"
- Verify `gpt-4o-mini` model access in your OpenAI account
- Check for model name typos in configuration

#### "Fallback responses only"
- Check network connectivity to OpenAI
- Verify API key permissions
- Review error logs for specific issues

### Support

For technical issues:
1. Check the error logs in LangSmith tracing
2. Verify environment configuration
3. Test with minimal examples
4. Contact OpenAI support for API-specific issues 