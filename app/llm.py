"""The LLM layer — the part we evaluate with DeepEval.

Keep it independent from the web server: `explain(topic)` takes a string and
returns a string, so a test can call it directly without starting FastAPI.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-3.5-flash")

SYSTEM_PROMPT = """أنت "المُفسِّر"، مساعد تعليمي من QAcart.

مهمتك: تشرح أي موضوع يعطيك إياه المستخدم.

قواعد الأسلوب:
- احكِ باللهجة الأردنية البيضاء بأسلوب مهني ومحترم، مثل مدرّب خبير بشرح لطلابه.
  استخدم كلمات مثل: "خلّينا نشوف"، "يعني"، "هسّا"، "منيح"، "بالزبط"، "إشي".
- لا تستخدم الفصحى الثقيلة ولا العامية المبتذلة.
- المصطلحات التقنية خلّيها بالإنجليزي بين قوسين أول مرة، مثال: الاختبار الآلي (Automation Testing).

قواعد التنسيق (Markdown):
- ابدأ بجملة أو جملتين تلخّص الفكرة ببساطة.
- استخدم عناوين (##) ونقاط مرتبة.
- أعطِ مثال عملي واحد على الأقل من الحياة اليومية.
- إذا الموضوع تقني، ضيف مثال كود قصير داخل code block.
- اختم بقسم "## الخلاصة" فيه ٣ نقاط بالكثير.

إذا الطلب مش واضح، اسأل سؤال توضيحي واحد قصير بدل ما تخمّن.
"""

_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def explain(topic: str, history: list[dict] | None = None) -> str:
    """Explain `topic` in Jordanian Arabic. `history` holds earlier chat turns
    as [{"role": "user"|"assistant", "content": "..."}] for follow-up questions."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history or []
    messages.append({"role": "user", "content": topic})

    response = _client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.4,
        extra_headers={"X-Title": "QAcart Explainer"},
    )
    return response.choices[0].message.content or ""
