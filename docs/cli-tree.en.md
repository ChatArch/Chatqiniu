# CLI Tree

This page lists implemented `chatqiniu` commands only. The tree is derived from the current CLI help surface. When a command changes, update this page, tests, and the reusable Python API together.

## Top-Level Commands

```text
chatqiniu
├── --version                    # print the package version
├── auth                         # credential login, cleanup, and read-only identity checks
├── profile                      # ChatEnv named profile management
├── config                       # default bucket / URL / CDN settings
├── bucket                       # inspect Kodo buckets
├── object                       # manage Kodo objects
├── url                          # generate object URLs
├── cdn                          # CDN refresh, prefetch, and task lookup
├── cert                         # inspect, upload, deploy, and delete CDN certificates
├── domain                       # inspect CDN domains and HTTPS settings
├── doctor                       # local diagnostics
├── docs                         # official links and examples
└── hello                        # template smoke compatibility command
```

## Authentication and Profiles

```text
chatqiniu auth
├── login                        # write Qiniu credentials into ChatEnv
├── logout                       # clear active credentials or remove a named profile
└── whoami                       # validate credentials through read-only bucket listing

chatqiniu profile
├── create                       # create a named profile
├── delete                       # delete a named profile
├── list                         # list named profiles
├── show                         # show active or named profile values with secrets masked
└── use                          # activate a named profile

chatqiniu config
├── get                          # read one non-sensitive setting
├── list                         # list non-sensitive settings
├── set                          # write one setting
└── unset                        # remove one setting
```

## Object Storage

```text
chatqiniu bucket
├── list                         # list accessible buckets
└── show                         # show basic bucket information

chatqiniu object
├── list                         # list objects in one bucket
├── stat                         # show object metadata
├── upload                       # upload one local file
├── upload-dir                   # recursively upload a directory
├── download                     # download an object through a generated URL
├── delete                       # delete one object, dry-run by default
├── batch-delete                 # delete by prefix, dry-run by default
├── copy                         # copy one object, dry-run by default
└── move                         # move one object, dry-run by default

chatqiniu url
├── public                       # generate a public object URL
└── private                      # generate a private signed object URL
```

## CDN and Domains

```text
chatqiniu cdn
├── refresh                      # refresh CDN cache, dry-run by default
├── prefetch                     # prefetch CDN resources, dry-run by default
└── task                         # query CDN task status

chatqiniu domain
├── list                         # list CDN domains
├── show                         # show one CDN domain
└── https
    └── set                      # set the HTTPS certificate, dry-run by default
```

## Certificates

```text
chatqiniu cert
├── list                         # list CDN certificates
├── show                         # show one certificate
├── upload                       # upload a PEM certificate, dry-run by default
├── deploy                       # upload a certificate and bind multiple CDN domains, dry-run by default
└── delete                       # delete one certificate, dry-run by default
```

`cert deploy` requires `--execute --yes` for real writes and does not print certificate bodies or private keys. See [certificate deployment](certificate-workflow.md) for the operational workflow.

## Diagnostics and Docs

```text
chatqiniu doctor
└── check                        # check local config and read-only API health

chatqiniu docs
├── links                        # print curated official documentation links
├── open                         # print one official documentation link by topic
└── examples                     # print common examples
```
