# Star Bank: connect a Google Sheet (about 10 minutes)

Until this is done, stars are saved on each device separately. Once it is done, every device shares one balance per child, and you can open the Sheet any time to see every star.

## 1. Make the Sheet
1. Go to [sheets.new](https://sheets.new) (signed in to your Google account).
2. Name it **Den Star Bank**.

## 2. Add the script
1. In the Sheet, choose **Extensions → Apps Script**.
2. Delete what is in `Code.gs` and paste in everything from [`Code.gs`](Code.gs) in this folder.
3. On the line `const PARENT_PIN = 'CHANGE-ME';`, change `CHANGE-ME` to a PIN only grown-ups know, keeping the quotes, for example `'5821'`. You will type it in the Star Bank to give out rewards.
4. Click **Save** (the disk icon).

## 3. Publish it as a web app
1. Click **Deploy → New deployment**.
2. Click the gear next to "Select type" and choose **Web app**.
3. Set **Execute as: Me**, and set **Who has access: Anyone**. The Den pages are a public website, so they can't sign in to Google.
4. Click **Deploy**, then **Authorize access**, and allow it. Google may warn that the app isn't verified. Choose **Advanced → Go to (project name)**. It's your own script.
5. Copy the **Web app URL**. It looks like `https://script.google.com/macros/s/AKfy…/exec`.

## 4. Send the URL to Claude
Paste the URL into the chat. Claude puts it into `stars.js`, and every device starts syncing. Any stars already saved on a device are uploaded the next time that child opens a deck on it.

## Good to know
- **The Sheet is the record.** The `Stars` tab gets one row per star event: who, when, which question, and how many stars. Rewards show as negative rows.
- **Changing the PIN later:** edit the PIN line, then choose **Deploy → Manage deployments → Edit (pencil) → Version: New version → Deploy**. The URL stays the same.
- **Safety:** anyone who digs the URL out of the page source could add stars, but they can't spend them without the PIN. That's fine for family rewards.
- **Daddy** and **Mommy** collect stars as beta testers.
