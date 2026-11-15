# Darhan Semiatov

Go backend · AI/LLM engineering · Almaty, Kazakhstan

I build Go services that run in production and the ML/LLM pieces around them: scoring models, LLM integrations, Telegram bots.
4th-year student at Narxoz University, intern at QazCode. Open to Go / AI roles from 2027.

### Featured

**[Tropa](https://130-61-149-209.sslip.io)**: a map of places around Almaty for going out with friends. It is live and has real users.
Go, html/template, PostgreSQL (pgx), migrations, SSE chats, Telegram notifications, rate-limited auth, admin moderation. Self-hosted with Docker and Caddy on an Oracle ARM VM, with nightly backups.

**IELTS writing scorer**: a fine-tuned DeBERTa-v3 regressor that scores essays on 4 criteria, exported to ONNX and served by a Python service that a Go app calls.
The LLM only explains the scores. It does not grade.

**[F1 race winner prediction](https://github.com/DarkIL1ght/ResearchF1Prediction)**: an ML study on historical Formula 1 data. It covers preprocessing, XGBoost, a custom race-level winner accuracy metric, feature importance and a temporal learning curve.

**Decentrathon 6.0**: I captained a team at a hackathon with about 1,500 participants. In 2 days we built a support copilot for a mobile operator: ticket category and priority classification, plus answers grounded in the knowledge base.

*Some of these repositories are private. Happy to walk through the code in an interview.*

### Stack

**Main:** Go · PostgreSQL · Docker · Linux · GitHub Actions · Caddy
**AI/ML:** Python · PyTorch · ONNX Runtime · LLM APIs (Claude, Gemini, Ollama)
**Also:** Java · JavaScript · SQL

### How I work

Layered architecture (domain → application → adapters), tests on every layer, an `architecture.md` in every repo, and CI before merge.

### Contact

[LinkedIn](https://www.linkedin.com/in/darhan-semiyatov-a5171b3a8) · [Semiatov@mail.ru](mailto:Semiatov@mail.ru)
