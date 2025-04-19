clients/ → direct HTTP API interaction

sources/ → logic to convert and prepare client data for pipelines

pipelines/ → orchestrate fetching and delegate saving to storage

storage/ → choose and abstract storage backend

core/registry.py → tracks where data is saved and maps storage per pipeline/source

core/scheduler.py → placeholder for cron/Airflow integration