# Shake Presentation Preflight Design

Status: Completed

## Problem

After a valid shake, the controller checks the retired Twitter session before
checking whether an alert or composer already owns presentation. Repeated shake
delivery can therefore touch account state even though no new UI work is
eligible.

## Options

1. Keep session lookup first and rely on later presentation rejection.
2. Reserve composer ownership before session lookup, then undo it for missing sessions.
3. Preflight visible idle presentation state before session lookup and recheck it when reserving the composer.

## Decision

Use option 3. It avoids unnecessary account access without reserving composer
state for the login-required alert path, and preserves the existing atomic
reservation immediately before composer construction.
