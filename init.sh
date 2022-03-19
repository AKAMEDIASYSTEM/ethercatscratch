#!/bin/bash
cp sar2022.service /etc/systemd/system/
cp sar2022.timer /etc/systemd/system/
systemctl enable sar2022.timer
systemctl start sar2022.timer
systemctl enable sar2022.service
systemctl start sar2022.service