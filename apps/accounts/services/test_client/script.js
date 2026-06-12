const REDIRECT_URI = "http://localhost:8080/callback";
const CLIENT_ID = "1501650689443500095";

const authUrl =
    "https://discord.com/oauth2/authorize?" +
    new URLSearchParams({
        client_id: CLIENT_ID,
        redirect_uri: REDIRECT_URI,
        response_type: "code",
        scope: "identify"
    });

window.location.href = authUrl;
