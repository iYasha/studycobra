#! /usr/bin/env bash
set -e

celery worker -A .worker -l info -Q main-queue -c 1
