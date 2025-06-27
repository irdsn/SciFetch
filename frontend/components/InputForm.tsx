// components/InputForm.tsx

import React from "react";

interface InputFormProps {
  prompt: string;
  setPrompt: (value: string) => void;
  apiKey: string;
  setApiKey: (value: string) => void;
  onSubmit: () => void;
}

const InputForm: React.FC<InputFormProps> = ({
  prompt,
  setPrompt,
  apiKey,
  setApiKey,
  onSubmit,
}) => {
  // Handles the form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
      <label htmlFor="prompt">Enter your scientific research prompt:</label>
      <br />
      <textarea
        id="prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="e.g., Cancer detection using AI"
        rows={3}
        style={{ width: "100%", padding: "0.5rem", fontSize: "1rem", marginTop: "0.5rem" }}
      />
      <br />
      <label htmlFor="apiKey" style={{ marginTop: "1rem", display: "block" }}>
        OpenAI API Key:
      </label>
      <input
        id="apiKey"
        type="password"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        placeholder="sk-..."
        style={{
          width: "100%",
          padding: "0.5rem",
          fontSize: "1rem",
          marginTop: "0.5rem",
        }}
      />
      <br />
      <div style={{ textAlign: "center", marginTop: "1rem" }}>
        <button
            type="submit"
            style={{
            padding: "0.5rem 1.5rem",
            fontSize: "2rem",
            backgroundColor: "#0070f3",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer"
            }}
            >
            🚀 Let’s Fetch!
        </button>
      </div>
    </form>
  );
};

export default InputForm;
