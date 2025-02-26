#include <WiFi.h>
#include <esp32cam.h>
#include <WebServer.h>

// Wi-Fi credentials
const char* WIFI_SSID = "Nointernet";
const char* WIFI_PASS = "";

// Web server on port 80
WebServer server(80);

// Set high-resolution image settings
static auto hiRes = esp32cam::Resolution::find(1024, 768);

// Function to capture and serve an image
void serveJpg() {
  auto frame = esp32cam::capture();
  if (!frame) {
    Serial.println("Capture failed");
    server.send(503, "text/plain", "Failed to capture image");
    return;
  }

  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");

  WiFiClient client = server.client();
  frame->writeTo(client);
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  // Configure camera
  esp32cam::Config cfg;
  cfg.setPins(esp32cam::pins::AiThinker);
  cfg.setResolution(hiRes);
  cfg.setJpeg(80);  // JPEG quality

  if (!esp32cam::Camera.begin(cfg)) {
    Serial.println("Camera init failed");
    while (true);
  }
  
  // Connect to Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected to Wi-Fi. IP: ");
  Serial.println(WiFi.localIP());

  // Set up web server routes
  server.on("/capture.jpg", serveJpg);
  server.begin();
  Serial.println("Server started");
}

void loop() {
  server.handleClient();
}
