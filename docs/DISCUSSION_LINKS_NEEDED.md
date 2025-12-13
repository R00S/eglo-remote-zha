# Request for Specific Discussion Links

## Current Situation

We need to find actual discussions about how the ERCU_3groups_Zm implements its 3 banks/groups functionality.

## Known Reference

The problem statement mentions:
> "https://community.home-assistant.io/t/eglo-connect-z-with-home-assistent-cant-find-a-way-to-make-them-usable-with-my-home-assistent/378439/17"

## What We Need

The user (@R00S) mentioned:
- "there are conclusions on how the three banks work on discussions on the internet"
- "my memory from reading the discussions is that it is unorthodox and may need special treatment"
- "search for discussion regarding this specific remote instead of theorising, the info is out there"

## Specific Information Needed

From these discussions, we need to find:

1. **How the buttons 1/2/3 actually work**:
   - Do they send Zigbee commands? If so, which ones?
   - Do they change remote state only?
   - Do they use a specific cluster or endpoint?

2. **The "unorthodox" implementation details**:
   - What makes it different from standard Zigbee groups?
   - Why does it need "special treatment"?
   - What have other users discovered?

3. **Implementation that works**:
   - Has someone gotten this working in ZHA or Zigbee2MQTT?
   - What approach did they use?
   - Any code examples or quirk implementations?

## Possible Discussion Locations

1. **Home Assistant Community Forum**:
   - Thread 378439 (provided)
   - Other Eglo/AwoX threads
   - ZHA integration discussions

2. **Zigbee2MQTT**:
   - GitHub issues
   - Device database entries
   - Converter implementations

3. **ZHA Device Handlers**:
   - GitHub issues/PRs
   - Discussions about AwoX devices
   - Similar remote implementations

4. **Reddit**:
   - r/homeassistant
   - r/zigbee
   - Search for "Eglo remote" or "ERCU_3groups"

## What Would Be Most Helpful

- Direct links to specific posts/comments that explain the implementation
- Quotes from users who figured it out
- Links to working quirk/converter code
- References to the specific mechanism used (e.g., "uses source endpoint switching", "requires group binding", etc.)

## Why This Matters

Without the actual implementation details from people who've studied this remote:
- We're guessing at the mechanism (Touchlink? Groups? Endpoints? Proprietary?)
- We can't implement a working quirk
- Users can't use the 3-bank functionality

---

**REQUEST**: Please provide links to or excerpts from the specific discussions that explain how the 3 banks work on this remote.
