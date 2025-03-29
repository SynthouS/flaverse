# Flaverse

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A secure anonymous chat application built with Flask and Supabase. Features dark theme, message linking, and real-time updates.

## Features

- Anonymous chat with auto-generated nicknames
- Supabase backend for message storage
- Dark theme with responsive design
- Message permalinks with copy functionality
- Rate limiting and input validation
- Real-time message updates
- Secure environment configuration

## Prerequisites

- Python 3.8+
- Supabase account
- Git
- PIP package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flaverse.git
cd flaverse
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create Supabase project:
   - Go to [Supabase Dashboard](https://supabase.com/dashboard/)
   - Create new project
   - Create `messages` table with:
     ```sql
     CREATE TABLE messages (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       nickname TEXT NOT NULL,
       message TEXT NOT NULL,
       created_at TIMESTAMPTZ DEFAULT NOW()
     );
     ```
   - Enable RLS with policies:
     ```sql
     CREATE POLICY "Allow public insert" ON messages FOR INSERT WITH CHECK (true);
     CREATE POLICY "Allow public select" ON messages FOR SELECT USING (true);
     ```

2. Create `.env` file:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
FLASK_ENV=development
```

## Running the Application

```bash
export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
flask run
```

Access the application at: `http://localhost:5000`

## Deployment

1. **Recommended Host**: [Render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Add environment variables:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `FLASK_ENV=production`

2. **Custom Domain** (Optional):
   - Configure DNS settings
   - Add SSL via Cloudflare
   - Set up proper caching headers

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Powered by [Supabase](https://supabase.com/)
- Icons by [Font Awesome](https://fontawesome.com/)
