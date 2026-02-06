import { useState } from 'react';
import { Upload, FileText, Activity, PieChart, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import './index.css';
import { translations } from './translations';

const API_BASE = import.meta.env.VITE_API_URL || "/api";

function App() {
  const [step, setStep] = useState('upload'); // upload, analyzing, dashboard
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [language, setLanguage] = useState('English');
  const [businessType, setBusinessType] = useState('Retail');
  const [error, setError] = useState('');

  const t = translations[language]; // Translation helper

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setStep('analyzing');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('business_type', businessType);
    formData.append('language', language);

    try {
      // Using native fetch for better debugging
      const res = await fetch(`${API_BASE}/analyze-file`, {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        let errorDetail = '';
        try {
          const errorJson = await res.json();
          errorDetail = errorJson.detail;
        } catch (e) {
          errorDetail = res.statusText;
        }
        throw new Error(`Server responded with ${res.status}: ${errorDetail}`);
      }

      const data = await res.json();
      setData(data);
      setStep('dashboard');
    } catch (err) {
      console.error(err);
      setError("Error: " + err.message + ". Check if backend (127.0.0.1:8000) is running.");
      setStep('upload');
    }
  };

  const downloadReport = () => {
    alert("Downloading report... (Feature mock)");
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="glass-panel" style={{ padding: '1rem 2rem', marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 className="text-gradient" style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{t.title}</h1>
        <button onClick={() => setLanguage(l => l === 'English' ? 'Hindi' : 'English')} className="glass-button" style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}>
          {t.switchBtn}
        </button>
      </header>

      {/* Main Content */}
      <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1rem' }}>

        {step === 'upload' && (
          <div className="glass-panel animate-fade-in" style={{ maxWidth: '600px', margin: '4rem auto', padding: '3rem', textAlign: 'center' }}>
            <div style={{ background: 'rgba(139, 92, 246, 0.1)', width: '80px', height: '80px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
              <Upload size={40} color="#8b5cf6" />
            </div>
            <h2 style={{ marginBottom: '1rem' }}>{t.uploadTitle}</h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
              {t.uploadDesc}
            </p>

            <form onSubmit={handleFileUpload}>
              <div style={{ marginBottom: '1.5rem', position: 'relative' }}>
                <input
                  type="file"
                  accept=".csv,.xlsx"
                  onChange={(e) => setFile(e.target.files[0])}
                  required
                  style={{ display: 'none' }}
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="glass-input" style={{ display: 'block', cursor: 'pointer', borderStyle: 'dashed', textAlign: 'center', padding: '2rem' }}>
                  {file ? file.name : t.selectFile}
                </label>
              </div>

              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Business Type</label>
                <select
                  className="glass-input"
                  style={{ width: '100%', padding: '0.8rem', background: 'rgba(255,255,255,0.05)', color: 'white', border: '1px solid rgba(255,255,255,0.1)' }}
                  onChange={(e) => setBusinessType(e.target.value)}
                  value={businessType}
                >
                  <option value="Retail">Retail Store / Shop</option>
                  <option value="Manufacturing">Manufacturing / Factory</option>
                  <option value="Agri">Agriculture / Farming</option>
                  <option value="Services">Service Business</option>
                  <option value="Logistics">Logistics / Transport</option>
                  <option value="Ecommerce">E-commerce / Online Store</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <button type="submit" className="glass-button" style={{ width: '100%' }}>
                {t.analyzeBtn}
              </button>
            </form>
            {error && <p style={{ color: 'var(--danger)', marginTop: '1rem' }}>{error}</p>}

            <div style={{ marginTop: '2rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
              <p>Try with sample data: <a href="http://127.0.0.1:8000/static/sample_statement.csv" style={{ color: 'var(--accent-primary)' }} download>{t.sampleLink}</a></p>
            </div>
          </div>
        )}

        {step === 'analyzing' && (
          <div style={{ textAlign: 'center', marginTop: '5rem' }}>
            <div className="spinner" style={{ width: '50px', height: '50px', border: '4px solid rgba(255,255,255,0.1)', borderTop: '4px solid var(--accent-primary)', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 2rem' }}></div>
            <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
            <h2>{t.analyzingTitle}</h2>
            <p style={{ color: 'var(--text-secondary)' }}>{t.analyzingDesc}</p>
          </div>
        )}

        {step === 'dashboard' && data && (
          <div className="animate-fade-in">
            {/* Top Stats */}
            <div className="dashboard-grid">
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <h3 style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{t.healthScore}</h3>
                <div style={{ fontSize: '3rem', fontWeight: 'bold', color: data.metrics.score > 70 ? 'var(--success)' : 'var(--warning)', margin: '0.5rem 0' }}>
                  {data.metrics.score}/100
                </div>
                <p>{t.status}: {data.metrics.readiness === 'High' ? t.creditReady : t.needsImprovement}</p>
              </div>

              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <h3 style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{t.netCashFlow}</h3>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', margin: '0.5rem 0' }}>
                  ₹{data.metrics.net_cash_flow.toLocaleString()}
                </div>
                <div style={{ display: 'flex', gap: '1rem', fontSize: '0.9rem' }}>
                  <span style={{ color: 'var(--success)' }}>{t.revenue}: {data.metrics.total_revenue.toLocaleString()}</span>
                  <span style={{ color: 'var(--danger)' }}>{t.expenses}: {data.metrics.total_expenses.toLocaleString()}</span>
                </div>
              </div>

              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <h3 style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{t.debtTax}</h3>
                <div style={{ marginTop: '0.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span>{t.debt}:</span>
                    <span style={{ fontWeight: 'bold' }}>₹{data.metrics.debt_obligations?.toLocaleString() || 0}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>{t.tax}:</span>
                    <span style={{ color: data.metrics.tax_compliance === 'Tax Payments Detected' ? 'var(--success)' : 'var(--warning)' }}>
                      {data.metrics.tax_compliance === 'Tax Payments Detected' ? t.taxDetected : data.metrics.tax_compliance}
                    </span>
                  </div>
                </div>
              </div>

              <div className="glass-panel" style={{ padding: '1.5rem', borderLeft: '4px solid var(--warning)' }}>
                <h3 style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{t.risks}</h3>
                <ul style={{ marginTop: '0.5rem', listStyle: 'none' }}>
                  {data.metrics.risks.length > 0 ? data.metrics.risks.map((risk, i) => (
                    <li key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                      <AlertTriangle size={14} color="#f59e0b" /> {risk}
                    </li>
                  )) : (
                    <li style={{ color: 'var(--success)' }}><CheckCircle size={14} /> {t.noRisks}</li>
                  )}
                </ul>
              </div>
            </div>

            {/* Charts & AI */}
            <div className="dashboard-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <h3>{t.cashFlowTrend}</h3>
                <div style={{ height: '300px', marginTop: '1rem' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data.metrics.monthly_trend}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis dataKey="date" stroke="#94a3b8" tickFormatter={(t) => new Date(t).toLocaleDateString(undefined, { month: 'short' })} />
                      <YAxis stroke="#94a3b8" />
                      <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none' }} />
                      <Line type="monotone" dataKey="credit" stroke="#10b981" strokeWidth={2} name={t.revenue} />
                      <Line type="monotone" dataKey="debit" stroke="#ef4444" strokeWidth={2} name={t.expenses} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                  <Activity size={20} color="#8b5cf6" />
                  <h3>{t.aiInsights}</h3>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '8px', whiteSpace: 'pre-wrap', lineHeight: '1.6', fontSize: '0.95rem' }}>
                  {data.insights}
                </div>
                {/* Product Recommendation Mock */}
                <div style={{ marginTop: '1.5rem' }}>
                  <h4 style={{ fontSize: '0.9rem', color: 'var(--accent-secondary)' }}>{t.recProducts}</h4>
                  <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '0.8rem', borderRadius: '8px', marginTop: '0.5rem', fontSize: '0.9rem' }}>
                    <strong>{t.workingCapitalLoan}:</strong> {t.loanDesc.replace('revenue', `₹${data.metrics.total_revenue.toLocaleString()}`)}
                  </div>
                </div>
              </div>
            </div>

            <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
              <button onClick={() => window.print()} className="glass-button">{t.downloadReport}</button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
