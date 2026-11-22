NEXTRADE — 400+ NSE STOCK EDITION

FILES
- app.py
- requirements.txt
- README.txt

LOCAL WINDOWS RUN
1. Extract this ZIP.
2. Open the extracted NexTrade folder.
3. Click File Explorer address bar, type cmd, press Enter.
4. Run:
   py -m pip install -r requirements.txt
   py -m streamlit run app.py

STOCK SEARCH
The stock dropdown is searchable: click it and type a company name or ticker. Examples:
- Vedanta / VEDL
- Hindustan Unilever / HINDUNILVR
- DCM Shriram / DCMSHRIRAM
The list contains 690 distinct NSE Yahoo Finance ticker symbols. This is a curated broad list, not a live official NSE constituent file. Some symbols can be renamed, suspended, or unavailable from Yahoo. The app reports data errors instead of fabricating values.

DATA / DAILY UPDATE BEHAVIOUR
- Uses yfinance to request actual Yahoo Finance daily history (3 years) and recent 5-minute candles.
- No synthetic/demo price data is intentionally generated.
- Daily data cache is 5 minutes; intraday cache is 90 seconds.
- Clicking Refresh market data clears cache; clicking Analyze stock fetches again.
- Freshness check displays latest daily candle date and blocks forecasts if data is clearly stale (older than 4 calendar days) or future-dated. Ambiguous older weekday dates are flagged for verification because NSE holidays are not built into the calendar.
- The app does NOT run an unattended end-of-day scheduler. On a hosted Streamlit app, after market close, open it and click Refresh then Analyze to get the latest completed daily candle. It cannot guarantee the provider has published today's candle immediately after close.
- This design avoids pretending that an app asleep/idle is fetching data in the background.

DEPLOYMENT / REMOTE ACCESS
Recommended: Streamlit Community Cloud. It hosts the Python app remotely; your laptop can be off and your dad can open the public URL. Requirements:
1. Push app.py and requirements.txt to a GitHub repository.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Create app; choose repo, branch main, file app.py; choose a memorable subdomain; Deploy.
4. Share the resulting https://YOUR-APP.streamlit.app URL.
Community Cloud free apps may hibernate after 12 hours without traffic; a visitor can wake a sleeping app. A first load may take a little time. This means the link is hosted remotely but is not guaranteed to stay continuously warm.
Official guide: https://docs.streamlit.io/deploy/streamlit-community-cloud

IMPORTANT LIMITS
- Yahoo Finance / yfinance is unofficial, can be delayed, incomplete, rate-limited or unavailable. Not a broker-grade live feed.
- Freshness checks are conservative and do not have a complete NSE holiday calendar. Confirm displayed candle date and provider availability.
- Probabilities are model estimates, not guarantees. Holdout metrics are not a full strategy backtest; fees, taxes, slippage, gaps and liquidity are not modeled.
- Entry/stop/targets are ATR-based reference levels, not guaranteed execution prices.
- No order placement, Zerodha connection, or specific options-chain forecasts.
