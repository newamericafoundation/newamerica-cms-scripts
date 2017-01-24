# Scripts for New America CMS

Random scripts for bulk DB updates

## Fix Link Types

Fixes [#1245](https://github.com/newamericafoundation/newamerica-cms/issues/1245) for legacy posts
- Swap out `os.getenv("LOCAL_DB_URL")` with one of the Environment variables below

### Environment variables:
```sh
export HEROKU_PRODUCTION_DB_URL=$(heroku config:get DATABASE_URL -a na-production)
export HEROKU_STAGING_DB_URL=$(heroku config:get DATABASE_URL -a na-staging)
export LOCAL_DB_URL=postgres://localhost:5432/newamericaprod
```
