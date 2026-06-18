from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import json

COMEPTY_AI_KEYWORDS = {
    'trending': [
        'Right now the hottest trends on Comepty are: eco-friendly products, digital downloads, and handmade crafts. Short-form video content is driving massive traffic to product pages. Consider adding a product demo video!',
        'Trending categories this week: Electronics accessories, Home decor, and Fitness gear. Products with 3+ images and a video get 4x more clicks.',
        'Viral marketing is big right now. Products tagged with #trending or #exclusive are getting boosted visibility on the Comepty feed.',
    ],
    'marketing': [
        'Top affiliate marketing tips: 1) Use high-quality images (first impressions matter), 2) Write benefit-focused descriptions (not just features), 3) Add your affiliate link to track conversions, 4) Share your product page on social media with a direct link.',
        'To grow on Comepty: post consistently, engage in comments, use trending tags, and ask happy customers to leave reviews. Products with 10+ comments rank higher in search.',
        'The best-performing listings on Comepty have: a catchy title, 3-5 images, 1 demo video, 5+ relevant tags, and a competitive price. Update your listing based on click analytics.',
    ],
    'video': [
        'TikTok-style videos are the #1 driver of product sales right now. Keep videos under 60 seconds, show the product in action, add text overlays with key benefits, and end with a clear call-to-action.',
        'Video tips for more sales: good lighting is everything, film in portrait mode for mobile viewers, show before/after results, and pin your best customer review video to the top.',
    ],
    'price': [
        'Pricing strategy: Research your competition, then price 5-10% lower to get your first sales. Once you have reviews and social proof, gradually increase your price. Products priced between $10–$50 convert best on Comepty.',
        'Psychological pricing tip: $19.99 outperforms $20 by 15%. Bundle products together for higher average order value. Offer a discount code in your bio to incentivize first-time buyers.',
    ],
    'grow': [
        'To grow your Comepty store fast: 1) Complete your profile with a real photo and bio, 2) Post 3-5 products per week, 3) Engage with other sellers comments, 4) Use the Comepty AI section for trending keywords, 5) Share your store link on Instagram and TikTok.',
        'Growth hack: Ask your first 10 customers to leave a comment on your product. Social proof is the single biggest conversion driver. Offer a small bonus or discount in exchange.',
    ],
    'seo': [
        'SEO tips for your Comepty listing: Include your main keyword in the title, first sentence of description, and tags. Use long-tail keywords like "handmade leather wallet for men" instead of just "wallet". This gets more targeted traffic.',
        'Tag strategy: Use a mix of broad tags (fashion, electronics) and specific tags (vintage leather, wireless charging). Aim for 7-10 tags per product for maximum discoverability.',
    ],
    'start': [
        'Getting started on Comepty: Create your profile, post your first product with great photos, set up your affiliate link, and share in your first social media post. Your first sale usually comes within 48 hours if you have a quality listing.',
        'New seller checklist: ✅ Complete profile ✅ Add profile photo ✅ Post 1st product with video ✅ Add affiliate link ✅ Get 3 tags minimum ✅ Share on social media. You are ready to sell!',
    ],
}

DEFAULT_RESPONSES = [
    "I'm Comepty AI 1.0! Ask me about trending products, marketing tips, pricing strategy, video content, or how to grow your store. I'm here to help you succeed!",
    "Try asking me: 'What's trending?', 'How do I market my product?', 'How do I grow my store?', or 'What's the best pricing strategy?'",
    "Great question! I specialize in helping Comepty sellers grow. Ask me about trends, marketing, SEO, video tips, or pricing to get started.",
]


def get_ai_response(message):
    message_lower = message.lower()

    if settings.OPENAI_API_KEY:
        try:
            import openai
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {
                        'role': 'system',
                        'content': (
                            'You are Comepty AI 1.0, a smart assistant for the Comepty marketplace platform. '
                            'You help sellers with trending product ideas, marketing strategies, affiliate marketing, '
                            'pricing, video content tips, and growing their online store. '
                            'Be concise, friendly, and actionable. Use bullet points when listing tips. '
                            'Keep responses under 200 words.'
                        )
                    },
                    {'role': 'user', 'content': message}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception:
            pass

    import random
    for keyword, responses in COMEPTY_AI_KEYWORDS.items():
        if keyword in message_lower:
            return random.choice(responses)

    return random.choice(DEFAULT_RESPONSES)


def ai_chat(request):
    return render(request, 'ai_section/chat.html')


@require_POST
def ai_ask(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
    except (json.JSONDecodeError, AttributeError):
        message = request.POST.get('message', '').strip()

    if not message:
        return JsonResponse({'response': 'Please type a message first!'})

    response = get_ai_response(message)
    return JsonResponse({'response': response})
