def load_theme():
    return """
    <style>
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .fade-in {
            animation: fadeIn 0.6s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card {
            background: #ffffff;
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }

        .rating-good { color: #22c55e; font-weight: 600; }
        .rating-mid  { color: #f59e0b; font-weight: 600; }
        .rating-bad  { color: #ef4444; font-weight: 600; }
        .meta-card {
            background: #f8fafc;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            border: 1px solid #e5e7eb;
            margin-bottom: 1rem;
        }

        .meta-label {
            font-size: 0.75rem;
            color: #6b7280;
            margin-bottom: 0.25rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .meta-value {
            font-size: 0.95rem;
            font-weight: 600;
            color: #111827;
        }
    </style>
    """
