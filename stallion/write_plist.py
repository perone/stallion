import sys

plist_sample_text="""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>Stallone</string>

    <key>ProgramArguments</key>
    <array>
        <string>{python}</string>
        <string>-m</string>
        <string>stallion.main</string>
    </array>

    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
""".strip()

sys.stdout.write(plist_sample_text.format(python=sys.executable))
