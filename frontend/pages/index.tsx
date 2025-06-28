// pages/index.tsx

import React, { useState } from "react";
import Head from "next/head";
import InputForm from "../components/InputForm";
import Footer from "../components/Footer";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [htmlPreview, setHtmlPreview] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRunAgent = async () => {
    setLoading(true);
    setError("");
    setHtmlPreview("");
    setDownloadUrl("");

    try {
      const response = await fetch("http://localhost:8000/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          prompt: prompt,
          api_key: apiKey
        })
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setHtmlPreview(data.html_preview);
      setDownloadUrl(data.download_url);
    } catch (err) {
      console.error(err);
      setError("❌ Failed to fetch results. Please check your API key and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>SciFetch</title>
        <meta name="description" content="Autonomous scientific research agent using LangChain & OpenAI" />
      </Head>
      <main style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem" }}>
        <h1 style={{ textAlign: "center", fontSize: "3.5rem", fontWeight: "bold", marginBottom: "2rem" }}>
          SciFetch
        </h1>

        <p style={{ color: "#444", marginBottom: "2rem" }}>
          SciFetch is an autonomous LangChain-based agent designed to search, summarize, and store scientific literature based on user-provided prompts. It intelligently selects the best academic APIs for each topic, provides a synthesized summary, and outputs results in PDF.
        </p>

        <InputForm
          prompt={prompt}
          setPrompt={setPrompt}
          apiKey={apiKey}
          setApiKey={setApiKey}
          onSubmit={handleRunAgent}
        />

        {loading && <p>⏳ Running agent...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {htmlPreview && (
          <>
            <div
              style={{
                marginTop: "3rem",
                padding: "2rem",
                border: "1px solid #ccc",
                borderRadius: "8px",
                backgroundColor: "#fefefe"
              }}
              dangerouslySetInnerHTML={{ __html: htmlPreview }}
            />

            {downloadUrl && (
              <div style={{ textAlign: "center", marginTop: "2rem" }}>
                <a
                  href={downloadUrl}
                  download
                  style={{
                    display: "inline-block",
                    fontSize: "1.5rem",
                    padding: "0.5rem 1rem",
                    backgroundColor: "#0070f3",
                    color: "white",
                    textDecoration: "none",
                    borderRadius: "6px"
                  }}
                >
                  💾 Download PDF Report
                </a>
              </div>
            )}
          </>
        )}

        <Footer />
      </main>
    </>
  );
}
