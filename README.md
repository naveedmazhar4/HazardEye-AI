# HazardEye - Autonomous Industrial Safety Monitoring

HazardEye is an AI-powered industrial safety monitoring application. It uses computer vision to detect hazards in images and live camera feeds, calculates risk levels, generates actionable safety plans, and can send real-time alerts via voice and WhatsApp. Users can also generate PDF safety reports.

---

## Features

* Detect multiple hazards including gas cylinders, electrical fires, industrial fires, and PPE violations.
* Calculate risk score and categorize risk levels.
* Generate action plans for detected hazards.
* Real-time live camera monitoring with alerts.
* Generate downloadable PDF safety reports.
* Alerts via voice and WhatsApp.
* User-friendly web interface using **Streamlit**.

---

## Project Structure

```
HazardEye/
├─ agents/
│  ├─ hazard_detection.py
│  ├─ risk_analysis.py
│  ├─ action_plan.py
│  ├─ report_generator.py
├─ utils/
│  ├─ alerts.py
│  ├─ voice.py
│  ├─ config.py
├─ assets/
│  └─ bg_welcome.jpg
├─ app.py
├─ hazard_model.pt
├─ yolov8n.pt
├─ hazard_data.yaml
├─ requirements.txt
├─ train_hazard_model.py
└─ README.md
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/HazardEye.git
cd HazardEye
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Set your OpenAI API key in a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

* Upload an image to detect hazards.
* Start live camera monitoring.
* Generate PDF reports for detected hazards.

---

## Deployment

* **Streamlit Cloud**: Add your `OPENAI_API_KEY` as a secret in Streamlit Cloud settings. `.env` is not required on deployment.
* **Hugging Face Spaces**: Add your API key as a secret variable in your Space settings.

---

## Notes

* Do **not** push your `.env` file or API keys to GitHub.
* Ensure all model files (`hazard_model.pt` and `yolov8n.pt`) are included in the repository.

---

## License

This project is licensed under the MIT License.

---

## Contact

For support:

**Email:** [support@hazardeye.com](mailto:support@hazardeye.com)
**Phone/WhatsApp:** +92-300-1234567

Follow us:

* [LinkedIn](https://www.linkedin.com/)
* [Twitter](https://twitter.com/)
* [GitHub](https://github.com/)
