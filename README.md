Why couldn't we just use the remote.http check instead? Why did you have to write a plugin for it?

most of our internal stuff could not benefit from remote monitors without work and vulnerabilities
but in addition, i realized the nature of our traffic doesn't really fit in with remote checks on internal sites, especially when we're trying to monitor things like our endpoints
that way we don't have to screw with firewalls and NATs for the most part

----

### Metrics

| Metric | Description | Type |
| ------ | ----------- | ---- |
| code   | Response code | string |
| bytes  | Length of response.text | uint32 |
| duration | Count of milliseconds the check took to complete | double |
| match | The string representing the body match specified | string |
