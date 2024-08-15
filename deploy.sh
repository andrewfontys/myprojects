#!/bin/bash


sudo systemctl daemon-reload
# restart the service
sudo systemctl restart nginx

sudo systemctl enable myproject.service
sudo systemctl start myproject.service