import { useMemo, useState } from "react";

const INCOME_OPTIONS = ["<2L", "2-5L", "5-10L", ">10L"];

const INITIAL_FORM = {
  land_area_acres: 5,
  crop_type: "Rice",
  repayment_history_score: 80,
  annual_income_band: "5-10L",
};

function App() {
  const [formData, setFormData] = useState(INITIAL_FORM);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [validationErrors, setValidationErrors] = useState([]);
  const [networkError, setNetworkError] = useState("");

  const prettyReasonCodes = useMemo(() => {
    if (!result?.reason_codes) {
      return [];
    }

    return result.reason_codes.map((code) => code.replaceAll("_", " "));
  }, [result]);

  const handleChange = (event) => {
    const { name, value, type } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: type === "number" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setResult(null);
    setValidationErrors([]);
    setNetworkError("");

    try {
      const response = await fetch("http://localhost:8000/score", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 422 && Array.isArray(data.detail)) {
          setValidationErrors(data.detail);
        } else {
          setNetworkError("The server returned an unexpected error.");
        }
        return;
      }

      setResult(data);
    } catch (error) {
      setNetworkError("Unable to connect to the backend. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <div className="card">
        <h1>Scoring Calculator</h1>
        <p className="subtitle">Submit farmer details to calculate a score.</p>

        <form className="score-form" onSubmit={handleSubmit}>
          <label>
            <span>Land Area (acres)</span>
            <input
              type="number"
              name="land_area_acres"
              min="0"
              step="0.01"
              value={formData.land_area_acres}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            <span>Crop Type</span>
            <input
              type="text"
              name="crop_type"
              value={formData.crop_type}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            <span>Repayment History Score</span>
            <input
              type="number"
              name="repayment_history_score"
              min="0"
              max="100"
              value={formData.repayment_history_score}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            <span>Annual Income Band</span>
            <select
              name="annual_income_band"
              value={formData.annual_income_band}
              onChange={handleChange}
            >
              {INCOME_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Calculating..." : "Calculate Score"}
          </button>
        </form>

        {validationErrors.length > 0 && (
          <div className="panel error-panel">
            <h2>Validation Errors</h2>
            <ul>
              {validationErrors.map((error, index) => (
                <li key={`${error.loc?.join("-")}-${index}`}>
                  {error.loc?.join(" → ")}: {error.msg}
                </li>
              ))}
            </ul>
          </div>
        )}

        {networkError && (
          <div className="panel error-panel">
            <h2>Error</h2>
            <p>{networkError}</p>
          </div>
        )}

        {result && (
          <div className="panel success-panel">
            <h2>Score Result</h2>
            <p>
              <strong>Score:</strong> {result.score}
            </p>
            <p>
              <strong>Request ID:</strong> {result.request_id}
            </p>
            <p>
              <strong>Timestamp:</strong> {result.timestamp}
            </p>
            <div>
              <strong>Reason Codes:</strong>
              <ul>
                {prettyReasonCodes.map((reason, index) => (
                  <li key={result.reason_codes[index]}>{reason}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
