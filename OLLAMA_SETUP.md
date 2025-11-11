# Ollama Setup for WSL

This guide explains how to use Ollama running on Windows from WSL.

## Problem

By default, Ollama on Windows listens only on `localhost:11434`, which is not accessible from WSL. WSL runs in a separate network namespace and needs to connect to the Windows host IP.

## Solution

Configure Ollama to listen on all network interfaces so WSL can connect.

## Setup Steps

### Step 1: Configure Ollama on Windows

**Option A: Using PowerShell (Recommended)**

1. Open PowerShell as Administrator
2. Run:
   ```powershell
   [System.Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'User')
   ```
3. Close PowerShell

**Option B: Using System Settings**

1. Open Windows System Settings
2. Search for "Environment Variables"
3. Click "Edit environment variables for your account"
4. Click "New" under User variables
5. Variable name: `OLLAMA_HOST`
6. Variable value: `0.0.0.0:11434`
7. Click OK

### Step 2: Restart Ollama

1. Close Ollama application completely (check system tray)
2. Restart Ollama from Start Menu
3. Verify it's running: Open browser to http://localhost:11434
   - Should see: "Ollama is running"

### Step 3: Configure blog-agent providers.yaml

The default configuration should work automatically. WSL will connect to Windows host at `10.255.255.254:11434`.

If needed, update `blog_agent/config/providers.yaml`:

```yaml
providers:
  ollama:
    model: llama3:latest
    host: http://10.255.255.254:11434  # Windows host IP from WSL
    max_tokens: 4000
    temperature: 0.7
```

### Step 4: Test Connection

Run the test script:

```bash
source .venv/bin/activate
python test_ollama.py
```

Expected output:
```
✅ Provider created: ollama
   Model: llama3:latest
   Host: http://10.255.255.254:11434

✅ Generation successful!
```

## Firewall Configuration (If Needed)

If the connection still fails, you may need to allow Ollama through Windows Firewall:

1. Open Windows Defender Firewall with Advanced Security
2. Click "Inbound Rules" → "New Rule"
3. Rule Type: Port
4. Protocol: TCP
5. Specific local ports: `11434`
6. Action: Allow the connection
7. Profile: Select all (Domain, Private, Public)
8. Name: "Ollama WSL Access"

## Troubleshooting

### Test Ollama from WSL

```bash
# Get Windows host IP
cat /etc/resolv.conf | grep nameserver

# Test connectivity (should return "Ollama is running")
curl http://10.255.255.254:11434
```

### Test Ollama from Windows

Open browser to: http://localhost:11434

Should see: "Ollama is running"

### Check Ollama is listening on 0.0.0.0

In PowerShell:
```powershell
netstat -ano | findstr :11434
```

Should show:
```
TCP    0.0.0.0:11434    0.0.0.0:0    LISTENING    <PID>
```

If it shows `127.0.0.1:11434` instead of `0.0.0.0:11434`, the environment variable didn't take effect. Restart Ollama.

## Using Ollama with blog-agent

### Option 1: Use in config.yaml (per-article)

```yaml
title: My Article
target_audience: Developers
tone: ekspercki, ale naturalny i rozmowny
model: llama3:latest  # Use Ollama model
```

Then run:
```bash
blog-agent create --config path/to/config.yaml --provider ollama
```

### Option 2: Use with CLI flag

```bash
blog-agent create --config path/to/config.yaml --provider ollama
```

### Available Ollama Models

Your installed models:
- `llama3:latest` - Meta Llama 3 (4.7 GB)
- `mistral:latest` - Mistral 7B (4.1 GB)
- `codellama:13b` - Code Llama 13B (7.4 GB)
- `codellama:7b` - Code Llama 7B (3.8 GB)
- `gemma3:4b` - Google Gemma 3 4B (3.3 GB)
- `gemma3:12b-it-qat` - Google Gemma 3 12B (8.9 GB)
- `phi3:mini` - Microsoft Phi-3 Mini (2.2 GB)
- `gpt-oss:20b` - GPT-OSS 20B (13 GB)

## Performance Notes

- **Local models** are free but slower than cloud APIs
- **Recommended for testing**: `llama3:latest`, `mistral:latest`
- **For production**: Use Claude (faster, better quality)
- **For code**: `codellama:13b` or `codellama:7b`
- **For speed**: `phi3:mini` (smallest, fastest)

## Security Note

Setting `OLLAMA_HOST=0.0.0.0:11434` makes Ollama accessible from your local network. If you're on a shared network, consider using firewall rules to restrict access to WSL only.

Alternative: Use `OLLAMA_HOST=10.255.255.254:11434` to bind to WSL interface only.
