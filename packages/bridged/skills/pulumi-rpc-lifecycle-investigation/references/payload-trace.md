# RPC Payload Trace

Which fields to pull out of a gRPC log, how to classify the values you find, and where to check lifecycle assumptions.

## Fields To Collect

Parse only the calls relevant to the resource under investigation, in order. For each relevant URN:

| Stage | Payload fields |
| :--- | :--- |
| Language host to engine | `RegisterResource.request.object`, dependencies, options, version, aliases, import ID, additional secret outputs |
| Provider config | `CheckConfig`, `Configure`, provider inputs |
| Resource validation | `Check.request.olds`, `Check.request.news`, `Check.response.inputs`, failures |
| Refresh and read | `Read.request.properties`, `Read.request.inputs`, `Read.response.properties`, `Read.response.inputs` |
| Diff | `Diff.request.olds`, `Diff.request.oldInputs`, `Diff.request.news`, ignore changes, response changes, detailed diff, errors |
| Execution | `Create`, `Update`, `Delete`, `Invoke`, or provider-specific calls if reached |

Do not summarize the whole log when one property or one operation explains the failure. Trace the smallest useful path.

## Classify Each Value By Source

For the failing property or decision, attribute every observed value:

| Source | Where it shows up |
| :--- | :--- |
| User program input | `RegisterResource.request.object` |
| Checked input | `Check.response.inputs` |
| Prior checkpoint input | `Check.request.olds`, `Read.request.inputs`, refresh `Diff.news` |
| Refreshed candidate | `Read.response.inputs` / `Read.response.properties` |
| Provider default or autonaming output | `Check` |
| Bridge translation artifact | Pulumi-to-TF config/state conversion |
| Upstream TF behavior | State upgraders, `CustomizeDiff`, plan modifiers, schema defaults, validators, CRUD |

Track unknown values, dependency substitution, and `ignoreChanges` preprocessing separately from provider defaults.

## Lifecycle Docs

Verify lifecycle assumptions against the Pulumi architecture docs before naming an owner. Prefer the Markdown source over rendered pages for search and selective reading.

Source order:

1. If a local `pulumi/pulumi` checkout is available, `rg` under `docs/architecture/` and read only the relevant file.
2. Otherwise use GitHub code search to locate the source path, then fetch only that Markdown file.
3. Use the rendered ReadTheDocs pages as a fallback, or as stable links when citing docs in a final report.

Useful source paths:

- Overview: `pulumi/pulumi:docs/architecture/README.md`
- Resource registration: `pulumi/pulumi:docs/architecture/deployment-execution/resource-registration.md`
- Provider implementer guide: `pulumi/pulumi:docs/architecture/providers/implementers-guide.md`

```bash
gh search code "RegisterResourceRequest path:docs/architecture" --repo pulumi/pulumi --limit 10 --json path,url
gh api repos/pulumi/pulumi/contents/docs/architecture/deployment-execution/resource-registration.md --jq '.content' | base64 -d | rg -n "Read|Diff|oldInputs|refresh"
gh api repos/pulumi/pulumi/contents/docs/architecture/providers/implementers-guide.md --jq '.content' | base64 -d | rg -n "Check|Diff|Read|Update"
```

Rendered links for final citations or fallback:

- `https://pulumi-developer-docs.readthedocs.io/latest/docs/architecture/README.html`
- `https://pulumi-developer-docs.readthedocs.io/latest/docs/architecture/deployment-execution/resource-registration.html`
- `https://pulumi-developer-docs.readthedocs.io/latest/docs/architecture/providers/implementers-guide.html`
