# 🚀 HR AI Toolkit: Resume Screener & Employee Sentiment Analysis

---

Welcome to the **HR AI Toolkit**! This project leverages the power of Google's **Gemini API** to bring intelligent automation to two critical HR functions: **resume screening** and **employee sentiment analysis**. Say goodbye to tedious manual tasks and hello to data-driven insights that can transform your recruitment and workplace culture.

## ✨ Project Highlights

In today's dynamic business landscape, attracting top talent and fostering a positive work environment are paramount. This toolkit provides innovative solutions to these challenges:

1.  **Smart Resume Screener:** Revolutionize your hiring process. This system intelligently filters resumes, matching candidates to job descriptions and desired skills, drastically cutting down on review time and accelerating time-to-hire.

2.  **Insightful Employee Sentiment Analysis:** Understand your team's pulse. By analyzing textual feedback, this system provides actionable insights into employee morale, helping you proactively address concerns and cultivate a thriving culture.

Both modules are built on the robust capabilities of the **Google Gemini API**, ensuring cutting-edge natural language understanding and generation.

## 🌟 Key Features

* **⚡ Intelligent Resume Matching:**

    * **Advanced AI-Powered Screening:** Go beyond keyword matching. The system understands the nuances of resumes and job descriptions to identify the best fit.

    * **Efficiency Booster:** Automate the initial sifting, allowing your HR team to focus on high-potential candidates.

    * **Customizable Criteria:** Adapt the screening parameters to perfectly align with any role's requirements.

* **💖 Automated Sentiment Detection:**

    * **Real-time Insights:** Quickly process large volumes of text data (surveys, feedback forms) to gauge collective sentiment.

    * **Granular Analysis:** Categorize sentiment as positive, negative, or neutral, and even identify underlying themes and pain points.

    * **Proactive Engagement:** Use data to inform HR strategies, improve employee satisfaction, and reduce attrition.

* **🧠 Gemini API at its Core:**

    * **State-of-the-Art NLP:** Utilizes the latest advancements in large language models for unparalleled accuracy in text comprehension.

    * **Scalable Performance:** Designed to handle varying workloads, from small teams to large enterprises.

* **🧩 Adaptable & Modular Design:**

    * **Future-Ready Architecture:** While current implementations offer different levels of modularity, the foundational design supports easy expansion and integration into existing HRIS platforms.

    * **Clear Separation of Concerns:** Components are designed to be distinct for easier understanding and maintenance (especially in the pipeline version).

## 🏛️ System Architecture & Implementation Approaches

This project offers two distinct pathways, catering to different development needs and stages:

---

### 1. The Complete Pipeline System (Experimental)

* **Vision:** This represents our ambitious goal: a fully integrated, end-to-end HR AI pipeline. It's designed with modularity, comprehensive logging, and sequential processing in mind, aiming for production-grade robustness.

* **Current Status:** This system is **experimental** and a work in progress. While it showcases the architectural blueprint for a scalable solution, its complete functionality and stability are under active development. You might encounter areas requiring debugging or further implementation.

* **Best For:** Developers and contributors who wish to delve into a more complex system, understand a potential full-scale deployment, and actively participate in refining and stabilizing a comprehensive HR AI workflow.

---

### 2. The Single Integrated System (Guaranteed Working)

* **Vision:** This approach prioritizes immediate, reliable functionality. It consolidates the core resume screening and sentiment analysis features into a simpler, more direct structure.

* **Current Status:** This version is **guaranteed to work out-of-the-box** for its core functionalities. It's optimized for quick deployment and immediate utility, focusing on delivering the promised AI capabilities without the overhead of extensive logging or complex pipeline stages.

* **Best For:** Users who need a functional, plug-and-play solution right away. Ideal for quick demonstrations, initial testing, or integration into environments where a streamlined, direct application is preferred.

---

The repository is structured to allow you to easily navigate between, or choose to utilize, the version that best suits your project's current requirements.

## 🛠️ Getting Started: Setup & Installation

Follow these steps to set up the project on your local machine:

1.  **Clone the Repository:**
    Get the code onto your system.
    ```bash
    git clone [https://github.com/KanishkJagya1/resume_screening.git](https://github.com/KanishkJagya1/resume_screening.git)
    cd resume_screening
    ```

2.  **Create a Virtual Environment (Highly Recommended):**
    Isolate your project dependencies to avoid conflicts.
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Install all necessary Python libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
    (💡 *Ensure your `requirements.txt` includes essential libraries such as `google-generativeai`, `pandas`, `scikit-learn`, etc., based on your specific code implementations.*)

## 🔑 Google Gemini API Key Configuration

This project requires access to the Google Gemini API. Here's how to configure your key:

1.  **Obtain Your API Key:**
    Visit the [Google AI Studio](https://aistudio.google.com/app/apikey) to generate your unique API key.

2.  **Securely Set Your API Key:**
    For security best practices, we recommend setting your API key as an environment variable:

    * **On macOS/Linux:**
        ```bash
        export GOOGLE_API_KEY="YOUR_API_KEY"
        ```
    * **On Windows (Command Prompt):**
        ```cmd
        set GOOGLE_API_KEY="YOUR_API_KEY"
        ```
    * **On Windows (PowerShell):**
        ```powershell
        $env:GOOGLE_API_KEY="YOUR_API_KEY"
        ```

    Alternatively, for development convenience (though less secure for production), you can place your API key directly in a `.env` file at the root of your project and load it using a library like `python-dotenv`.

## 🚀 How to Use

Usage varies depending on the system you choose. Navigate to the respective directories for detailed instructions and examples.

### Using the Single Integrated System (Recommended for Quick Start)

* **Location:** Navigate to the directory containing the integrated system's code (e.g., `src/integrated_system/`).

* **Execution:** Run the main script, typically from your terminal:

    ```bash
    python your_main_integrated_script.py # Replace with your actual script name, e.g., main_app.py
    ```

* **Interaction:** The script will likely guide you through prompts for inputs like resume file paths, job description text, or employee feedback data. Refer to the script's internal comments or companion documentation for specific usage details.

### Exploring the Complete Pipeline System (For Developers & Experimenters)

* **Location:** Dive into the directories structured for the pipeline (e.g., `src/pipeline/data_ingestion/`, `src/pipeline/screening_module/`, etc.).

* **Execution Flow:** Each stage of the pipeline (e.g., data ingestion, processing, analysis, logging) will have its own script. You'll generally run these in sequence.

* **Development Note:** Be prepared for an exploration and debugging journey. This system is a blueprint for a more robust, scalable architecture, and may require further development to be fully operational.

## 🤝 Contributing to the Project

We welcome contributions from the community! If you'd like to improve this HR AI Toolkit, please follow our contribution guidelines:

1.  **Fork** the repository to your GitHub account.

2.  **Create a new branch** for your feature or bug fix:

    ```bash
    git checkout -b feature/your-awesome-feature
    # or
    git checkout -b bugfix/resolve-issue-xyz
    ```

3.  **Make your changes**, ensuring your code adheres to best practices and includes comprehensive comments.

4.  **Commit your changes** with a clear and concise message:

    ```bash
    git commit -m 'feat: Add new advanced resume parsing logic'
    ```

5.  **Push your changes** to your forked repository:

    ```bash
    git push origin feature/your-awesome-feature
    ```

6.  **Open a Pull Request** against the `main` branch of this repository. Describe your changes thoroughly and link to any relevant issues.

## 📄 License

This project is open-source and distributed under the **MIT License**. See the [LICENSE](LICENSE) file in the repository root for more details.

---

Made with ❤️ by Kanishk Jagya