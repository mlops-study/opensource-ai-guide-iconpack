#!/usr/bin/env bash
# 부록 G. Ollama 이미지 생성 오류 해결하기 — Homebrew용 v0.32.5 재설치 스크립트
#
# Ollama가 v0.32.6부터 이미지 생성 기능을 일시 제거하면서 생긴 문제를 우회하기 위해,
# Homebrew로 v0.32.5(이미지 생성을 지원하는 마지막 버전)를 설치하고 자동 업그레이드를 막는다.
#
# 사용법:
#   bash install_ollama_0325.sh
set -e

echo "1/3 기존 Ollama 서비스 중지 및 제거..."
brew services stop ollama 2>/dev/null || true
brew uninstall ollama 2>/dev/null || true

echo "2/3 Ollama v0.32.5 설치..."
brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/8951566dc5fa72925e694c67bbe55bf4e527bb9d/Formula/o/ollama.rb

echo "3/3 자동 업그레이드로 최신 버전이 되는 것 방지 (brew pin)..."
brew pin ollama

brew services start ollama

echo "완료. 'ollama --version'으로 0.32.5가 맞는지 확인한다."
