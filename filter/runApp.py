import subprocess
import os

def findNdLaunch(appName="YouTube Music"):
  commanPaths = [
    os.path.expandvars(rf'%LOCALAPPDATA%\Programs\YouTube Music\YouTube Music.exe'),
    os.path.expandvars(rf'%LOCALAPPDATA%\{appName}\{appName}.exe'),
    os.path.expandvars(rf'%APPDATA%\{appName}\{appName}.exe'),
  ]

  for path in commanPaths:
    if os.path.exists(path):
      print(f"Found: {path}")
      subprocess.Popen([path])
      return True
  print(f"{appName} desktop app not found, using browser streaming.")
  return False
