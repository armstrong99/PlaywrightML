#!/bin/bash

echo "::::: Installing Dependencies :::::"
pip install -r requirements.txt

echo "::::: Installing Playwright Browser :::::"
python -m playwright install || python3 -m playwright install

echo "::::: Setup Complete :::::"
