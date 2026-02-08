# Local 10FastFingers-style Typing Test (Flask)

A simple Flask web app inspired by 10FastFingers.

- Login with **username only** (no password)
- Choose test duration (1/2/5/10 minutes)
- Type a stream of random words (from a fixed wordlist)
- Live feedback: correct words **green**, wrong words **red**
- Shows **current word + next 20 words**
- End-of-test stats: correct, wrong, total, WPM, accuracy
- Saves results to a local **SQLite** database
- History page with a **progress graph** (WPM + Accuracy)

## Project Structure

```
local_10_fast_fingers/
├─ app.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ .dockerignore
├─ README.md
└─ templates/
   ├─ login.html
   ├─ dashboard.html
   ├─ test.html
   └─ history.html
```

When you run the app for the first time, Flask/SQLAlchemy will create a local SQLite database at:

- `instance/typing_test.db`

## Requirements

- Python 3.9+ recommended
- Linux / WSL / macOS / Windows (WSL works well)

Python dependencies are listed in `requirements.txt`.

## Setup (venv)

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open:

- http://localhost:5000

## How to Use

1. Open the app and enter a username.
2. Choose a duration (1, 2, 5, or 10 minutes).
3. Start typing.
   - Press **Space** after each word to submit it.
   - The current word is highlighted.
   - Correct words turn green; wrong words turn red.
4. When time ends, results are shown and saved automatically.
5. Visit **History** to see your progress chart + all test results.

---

## Docker Setup

### Prerequisites

**Important:** For Docker/NAS deployment, make sure `app.py` binds to all interfaces:

```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
```

Without `host="0.0.0.0"`, Flask only listens on localhost inside the container and won't be accessible from outside.

### Quick Start (Local Docker)

#### Build the image
```bash
docker build -t typing-test:latest .
```

#### Run the container
```bash
docker run -d --name typing-test-app -p 5000:5000 typing-test:latest
```

#### Access the app
Open your browser:
- http://localhost:5000

### Persistent Database (Recommended)

The SQLite database is stored at `/app/instance/typing_test.db` inside the container.

**Without a volume/bind-mount, you lose all history when the container is recreated.**

#### Option A: Named volume (easiest)
```bash
docker run -d \
  --name typing-test-app \
  -p 5000:5000 \
  -v typing-test-data:/app/instance \
  typing-test:latest
```

#### Option B: Bind mount (store DB in a specific host folder)
```bash
docker run -d \
  --name typing-test-app \
  -p 5000:5000 \
  -v "$(pwd)/instance:/app/instance" \
  typing-test:latest
```

### Docker Compose

If you have `docker-compose.yml`:

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

### Push to Docker Hub

#### 1. Check your local image name
```bash
docker images
```

If built with `docker-compose`, the image might be named something like:
- `local_10_fast_fingers-typing-test:latest`

#### 2. Tag the image for Docker Hub
```bash
docker tag local_10_fast_fingers-typing-test:latest <dockerhub_user>/typing-test:latest
```

Replace `<dockerhub_user>` with your Docker Hub username (e.g., `lucahardonk`).

#### 3. Login and push
```bash
docker login
docker push <dockerhub_user>/typing-test:latest
```

### Pull and Run on NAS or Remote Server

#### 1. Pull the image
```bash
docker pull <dockerhub_user>/typing-test:latest
```

If the repository is private, login first:
```bash
docker login
```

#### 2. Run with persistent storage
```bash
docker run -d \
  --name typing-test-app \
  -p 5000:5000 \
  -v typing-test-data:/app/instance \
  <dockerhub_user>/typing-test:latest
```

#### 3. Access from your network
Open in your browser:
- `http://<NAS_IP>:5000`

Replace `<NAS_IP>` with the IP address of your NAS or server.

### TrueNAS SCALE Setup

#### Using the "Install Custom App" UI

**Image Configuration:**
- **Repository**: `<dockerhub_user>/typing-test`
- **Tag**: `latest`
- **Pull Policy**: `IfNotPresent`

**Container Configuration:**
- **Timezone**: Choose your timezone (e.g., `Europe/Rome`)
- **Restart Policy**: `Unless Stopped`

**Network Configuration:**
- **Host Network**: OFF
- **Ports**: Add port mapping
  - **Container Port**: `5000`
  - **Host Port**: `5000`
  - **Protocol**: `TCP`

**Storage Configuration (Important!):**

1. **Create the host folder** (via SSH or TrueNAS UI):
   ```bash
   sudo mkdir -p /mnt/nvme_pool/configurations/typing-test/instance
   ```

   Replace `nvme_pool` with your actual pool name.

2. **Add storage mapping**:
   - **Type**: `Host Path (Path that already exists on the system)`
   - **Host Path**: `/mnt/nvme_pool/configurations/typing-test/instance`
   - **Mount Path**: `/app/instance`
   - **Read Only**: OFF

**Why map `/app/instance`?**  
The Flask app writes the SQLite database to `/app/instance/typing_test.db` inside the container. By mounting this path to a NAS dataset, the database persists across container updates/restarts. Without this mapping, all test history is lost when the container is recreated.

#### Using Docker CLI on TrueNAS SCALE

```bash
# Create the storage folder
sudo mkdir -p /mnt/nvme_pool/configurations/typing-test/instance

# Pull and run
sudo docker pull <dockerhub_user>/typing-test:latest

sudo docker run -d \
  --name typing-test-app \
  -p 5000:5000 \
  -v /mnt/nvme_pool/configurations/typing-test/instance:/app/instance \
  --restart unless-stopped \
  <dockerhub_user>/typing-test:latest
```

---

## Database

The app uses **SQLite** with **SQLAlchemy ORM**.

### Tables

#### `user`
- `id` (primary key)
- `username` (unique)

#### `test_result`
- `id` (primary key)
- `user_id` (foreign key → `user.id`)
- `duration` (test duration in seconds)
- `correct_words` (number of correct words)
- `wrong_words` (number of wrong words)
- `total_words` (total words typed)
- `wpm` (words per minute)
- `accuracy` (percentage)
- `timestamp` (when the test was taken)

### Inspect the Database

```bash
sqlite3 instance/typing_test.db
```

```sql
.tables
.schema user
.schema test_result
SELECT * FROM user;
SELECT * FROM test_result;
.quit
```

---

## Git Best Practices

### What NOT to commit

Create a `.gitignore` file:

```
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
instance/
*.db
.DS_Store
```

### What TO commit

- `app.py`
- `requirements.txt`
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `templates/`
- `README.md`
- `.gitignore`

**Never commit:**
- `.venv/` (virtual environment - not portable, platform-specific)
- `instance/` (database folder - contains user data)
- `*.db` (database files)

### Sharing the Project

Share the code (not the venv or database):

**Option 1: Via Git**
1. Push to Git (GitHub, GitLab, etc.)
2. Others clone and run:
   ```bash
   git clone <your-repo-url>
   cd local_10_fast_fingers
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

**Option 2: Via Docker Hub**
```bash
docker pull <dockerhub_user>/typing-test:latest
docker run -d -p 5000:5000 -v typing-test-data:/app/instance <dockerhub_user>/typing-test:latest
```

---

## Stats Explained

- **WPM (Words Per Minute)**: `(correct_words / duration_in_minutes)`
- **Accuracy**: `(correct_words / total_words) × 100%`
- **Total Words**: `correct_words + wrong_words`

---

## Troubleshooting

### Can't connect to the app (Docker)
Make sure `app.py` uses:
```python
app.run(host="0.0.0.0", port=5000, debug=False)
```

Check container logs:
```bash
docker logs typing-test-app
```

### Port already in use
Change the host port:
```bash
docker run -d -p 8080:5000 --name typing-test-app typing-test:latest
```
Then access at `http://localhost:8080`

### Database not persisting (Docker)
Make sure you're using a volume or bind mount:
```bash
-v typing-test-data:/app/instance
```

Check if the volume exists:
```bash
docker volume ls
docker volume inspect typing-test-data
```

### Permission errors on NAS
If you get permission errors writing to the bind-mounted folder:

```bash
sudo chmod -R 777 /mnt/nvme_pool/configurations/typing-test/instance
```

Or run container with specific user:
```bash
docker run -d \
  --name typing-test-app \
  -p 5000:5000 \
  -v /mnt/nvme_pool/configurations/typing-test/instance:/app/instance \
  --user $(id -u):$(id -g) \
  typing-test:latest
```

---

## License

This project is open source. Feel free to modify and distribute.

---

## Credits

Inspired by [10FastFingers](https://10fastfingers.com/).
