# 🤖 AI Resume Analyzer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-link.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

An intelligent AI-powered resume analyzer that helps job seekers optimize their resumes for specific job roles. The tool provides detailed ATS (Applicant Tracking System) compatibility analysis, skill gap identification, and actionable recommendations to improve your chances of getting shortlisted.

---

## ✨ Features

### 📄 Resume Upload & Analysis
- Upload your resume in **PDF format** (max 20MB)
- Paste the **target job description** for comparison
- **Real-time analysis** with progress indicator

### 📊 Comprehensive Analytics Dashboard
| Metric | Description |
|--------|-------------|
| **Overall Match Score** | Weighted average of all metrics |
| **ATS Compatibility** | Keyword alignment with job description |
| **Skill Match Score** | Percentage of required skills found |
| **Content Quality** | Action verbs and measurable outcomes |

### 🔍 Skill Alignment
- ✅ **Matched Skills** – Skills found in your resume
- ❌ **Missing Key Skills** – Skills required by the job but not found
- 📈 **Skill Gap Analysis** – Identify areas for improvement

### 💡 Actionable Recommendations
- **Priority-based suggestions** (HIGH, MEDIUM, LOW)
- **Category-wise insights** (Technical Skills, Experience, Content, etc.)
- **Truthful advice** – Never suggests adding skills you don't have

### 📥 PDF Report Download
- Download a complete **analysis report** as PDF
- Includes all scores, skills, and recommendations

### 🎨 Theme Support
- 🌙 **Dark Mode** – Default theme with purple accents
- ☀️ **Light Mode** – Clean white theme with purple accents
- Toggle themes using the switch in the top-right corner

### 📱 Responsive Design
- Works seamlessly on **desktop, tablet, and mobile**
- **Adaptive layout** – Cards stack on zoom/mobile

---

## 🖥️ Live Demo

Check out the live demo: [AI Resume Analyzer](https://your-app-link.streamlit.app)

---

## 📸 Screenshots

### Dark Mode
![Dark Mode](screenshots/dark-mode.png)

### Light Mode
![Light Mode](screenshots/light-mode.png)

### Analysis Results
![Results](screenshots/results.png)

### Mobile View
![Mobile View](screenshots/mobile-view.png)

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Frontend** | Streamlit, HTML, CSS, JavaScript |
| **Backend** | Python 3.10+ |
| **PDF Processing** | PyPDF2 / pypdf |
| **PDF Report Generation** | FPDF2 |
| **Font** | Comfortaa (Google Fonts) |
| **Styling** | Custom CSS with Dark/Light themes |
| **Deployment** | Streamlit Cloud / Hugging Face Spaces |

---

## 📁 Project Structure

```
AI-Resume-Analyzer/
│
├── frontend/
│   ├── app.py                      # Main Streamlit application
│   ├── themes.py                   # Light/Dark theme management
│   ├── backend/
│   │   └── analyzer.py             # Resume analysis logic
│   └── requirements.txt            # Python dependencies
│
├── data/
│   └── jd.txt                      # Sample job description
│
├── screenshots/                    # Application screenshots
│   ├── dark-mode.png
│   ├── light-mode.png
│   ├── results.png
│   └── mobile-view.png
│
├── README.md                       # Project documentation
├── LICENSE                         # MIT License
└── .gitignore                      # Git ignore file
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### Step 2: Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
cd frontend
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

### Step 5: Open Your Browser

Navigate to `http://localhost:8501`

---

## 📦 Dependencies

### `requirements.txt`

```txt
streamlit>=1.28.0
pypdf>=3.17.0
fpdf2>=2.7.0
pandas>=2.0.0
numpy>=1.24.0
```

### Install All Dependencies

```bash
pip install -r requirements.txt
```

---

## 🎯 How It Works

### 1. Upload Resume
- Click the dropzone or drag & drop your PDF resume
- File chip appears with filename and size
- Remove button (✕) to clear the file

### 2. Enter Job Description
- Paste the job description you're targeting
- The textarea expands to fit the content

### 3. Analyze
- Click **"✦ Analyze My Resume"**
- The analysis runs and results appear automatically

### 4. Review Results
- **Overall Score** – Circle indicator with percentage
- **Sub-scores** – ATS, Skill Match, Content Quality
- **Matched Skills** – Skills found in your resume
- **Missing Skills** – Skills required by the job
- **Recommendations** – Priority-based improvements

### 5. Download Report
- Click **"📥 Download Analysis Report"**
- A professional PDF report is generated

### 6. Analyze Another Resume
- Click **"🔄 Analyze Another Resume"**
- Clears previous results and returns to upload section

---

## 📊 Analysis Metrics Explained

### Overall Score
- Weighted combination of all metrics
- Range: 0-100
- **80+** – Excellent Match
- **65-79** – Good Match
- **50-64** – Moderate Match
- **Below 50** – Needs Improvement

### ATS Score
- Keyword alignment with job description
- Uses a comprehensive skill database
- Range: 0-100

### Skill Match Score
- Percentage of required skills found in resume
- Identifies matched and missing skills
- Range: 0-100

### Content Quality Score
- Action verbs used (e.g., Developed, Designed)
- Measurable outcomes (e.g., "increased by 20%")
- Resume length and structure

---

## 🎨 Theme Customization

### Dark Mode (Default)
- Background: `#0d0714`
- Cards: `#1a0f2e`
- Text: `#f1eefc`
- Accent: `#c084fc`

### Light Mode
- Background: `#f5f0ff`
- Cards: `#ffffff`
- Text: `#1a0f2e`
- Accent: `#7c3aed`

### Toggle Theme
- Click the **☀️/🌙** toggle in the top-right corner
- Theme preference is saved in session state

---

## 📱 Mobile Responsiveness

The app is fully responsive:
- Cards stack vertically on smaller screens
- Text adjusts for readability
- Toggle remains accessible
- Smooth scrolling between sections

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

### 1. Fork the Repository
Click the **Fork** button on GitHub

### 2. Create a New Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Follow the existing code style
- Update documentation if needed
- Test your changes locally

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: Add your feature description"
```

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Open a Pull Request

Go to the original repository and click **New Pull Request**

---

## 🧪 Running Tests

```bash
# Run the app locally
streamlit run app.py

# Test different features
# - Upload a PDF
# - Paste a job description
# - Click analyze
# - Download report
# - Switch themes
```

---

## 🚀 Deployment

### Option 1: Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click **"New app"**
5. Select your repository
6. Click **"Deploy"**

### Option 2: Hugging Face Spaces

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Choose **Streamlit** SDK
4. Upload your files
5. Click **"Create"**

### Option 3: Render

1. Go to [render.com](https://render.com)
2. Click **"New +" → "Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port 10000`
5. Click **"Create Web Service"**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) – For the amazing web framework
- [Google Fonts](https://fonts.google.com/) – For the Comfortaa font
- [Font Awesome](https://fontawesome.com/) – For icons
- [PyPDF2 / pypdf](https://pypi.org/project/pypdf/) – For PDF text extraction
- [FPDF2](https://pypi.org/project/fpdf2/) – For PDF report generation

---

## 📧 Contact

- **Your Name** – [your-email@example.com](mailto:your-email@example.com)
- **GitHub** – [@yourusername](https://github.com/yourusername)
- **LinkedIn** – [Your Profile](https://linkedin.com/in/yourprofile)
- **Portfolio** – [your-portfolio.com](https://your-portfolio.com)

---

## ⭐ Support

If you find this project helpful, please give it a ⭐ on GitHub!

---

## 🔮 Future Improvements

- [ ] Support for `.docx` resume format
- [ ] Integration with LinkedIn profile import
- [ ] Industry-specific skill databases
- [ ] Multi-language support
- [ ] Resume template suggestions
- [ ] Interview preparation tips
- [ ] Export to multiple formats (JSON, CSV)
- [ ] Historical analysis tracking
- [ ] User accounts and saved analyses
- [ ] Comparison with industry benchmarks

---

## 🐛 Known Issues

- None currently. Please report any issues via GitHub Issues.

---

## 📝 Changelog

### v1.0.0 (September 2024)
- Initial release
- Core resume analysis functionality
- Dark/Light theme support
- PDF report download
- Responsive design

---

## 👥 Contributors

- [Your Name](https://github.com/pothulayashwanth) - Creator & Maintainer

---

## 🛡️ Security

- Resume files are processed locally and **not stored** on servers
- Temporary files are deleted after analysis
- No data is shared with third parties

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/pothulayashwanth/ai-resume-analyzer)
![GitHub forks](https://img.shields.io/github/forks/pothulayashwanth/ai-resume-analyzer)
![GitHub issues](https://img.shields.io/github/issues/pothulayashwanth/ai-resume-analyzer)

---

**Made with ❤️ by Yashwanth Pothula**
