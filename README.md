\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}
\usepackage{xcolor}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue
}

\title{\textbf{EquiNova: A Smart Stock Analysis and Forecasting Platform}}
\author{Likhitha Marrapu}
\date{}

\begin{document}

\maketitle

\section*{🌐 Live Demo}
Experience the platform here: \\
\href{https://equinovastockanalysis-mywkt7xwpcqhfycgfhyjjj.streamlit.app/}{\texttt{https://equinovastockanalysis.streamlit.app}}

\section*{🔍 Project Overview}
\textbf{EquiNova} is an end-to-end, interactive stock analytics and forecasting platform developed in \texttt{VS Code} using \texttt{Streamlit}. It leverages real-time data from \texttt{Yahoo Finance} to deliver dynamic visualizations, anomaly detection, and intelligent forecasting for better trading decisions.

\vspace{0.5em}
\textit{Purpose:} Empower users to understand market behavior, detect unusual movements, and anticipate future trends through an intuitive, AI-assisted interface.

\section*{🚀 Key Features}
\begin{itemize}
    \item \textbf{Market Pulse:} View company insights, financial ratios, and interactive charts including RSI, MACD, and Moving Averages.
    \item \textbf{Price Forecast:} Predict next 30-day closing prices with ARIMA-based time series models, evaluated using RMSE.
    \item \textbf{Trade Alert:} Detect anomalies (spikes/dips) using Z-score with emoji markers and dynamic chart insights.
    \item \textbf{Live Index Snapshot:} Real-time updates for S\&P 500, NASDAQ, DOW JONES, and VIX with percentage movement indicators.
\end{itemize}

\section*{🧠 Technologies and Tools}
\begin{itemize}
    \item \textbf{Frontend/UI:} Streamlit, HTML/CSS, PIL
    \item \textbf{Backend/Data Handling:} yfinance, pandas, numpy
    \item \textbf{Statistical Modeling:} ARIMA (via statsmodels), Z-score, StandardScaler
    \item \textbf{Visualization:} Plotly (line charts, candlesticks, tables, anomaly markers)
    \item \textbf{Development Environment:} Visual Studio Code (VS Code)
\end{itemize}

\section*{📂 Project Structure}
\begin{itemize}
    \item \texttt{Trading\_App.py} \hfill --- Home page with live index and navigation
    \item \texttt{market\_pulse.py} \hfill --- Stock performance and indicator dashboard
    \item \texttt{price\_forecast.py} \hfill --- ARIMA-based forecasting and evaluation
    \item \texttt{trade\_alert.py} \hfill --- Real-time anomaly detection via Z-score
    \item \texttt{utils/} \hfill --- Utility scripts for modeling and visualization
\end{itemize}

\section*{📈 Forecasting Logic}
Forecasting is driven by the \textbf{ARIMA} algorithm, which models trends in historical closing prices after performing stationarity checks. Outputs are inverse-transformed and paired with RMSE metrics to ensure accurate, interpretable results.

\section*{📌 How to Run Locally}
\begin{verbatim}
git clone https://github.com/your-username/equinova.git
cd equinova
pip install -r requirements.txt
streamlit run Trading_App.py
\end{verbatim}

\section*{📫 Author}
Created with 💡 by \textbf{Likhitha Marrapu} \\
\href{https://www.linkedin.com/in/likhitha-marrapu-9964001b4/}{LinkedIn} |
\href{https://github.com/lmarrapu}{GitHub}

\end{document}
