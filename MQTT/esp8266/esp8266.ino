// #include <ESP8266WiFi.h>
// #include <PubSubClient.h>
// #include <DHT.h>
// #include <ArduinoJson.h>
// #include <WiFiUdp.h>
// #include <NTPClient.h>
// #include <time.h>

// // Định nghĩa chân cho DHT11, LED và quang trở
// #define DHTPIN D4       // Chân DHT11
// #define DHTTYPE DHT11   // Loại cảm biến DHT11
// #define LED1 D1        // LED 1
// #define LED2 D2        // LED 2
// #define LED3 D3        // LED 3
// #define LDR_PIN A0     // Chân quang trở

// // Thông tin kết nối WiFi và MQTT Broker
// const char* ssid = "WiFi";            // Thay bằng SSID của bạn
// const char* password = "01032000";    // Thay bằng mật khẩu WiFi của bạn
// const char* mqtt_server = "192.168.1.175";
// //const char* ssid = "12";            // Thay bằng SSID của bạn
// //const char* password = "namdinh1";  
 
// //const char* mqtt_server = "192.168.0.115"; 
// // const char* ssid = "CSFR0508";  
// // const char* password = "nhungtran1997";  
// // const char* mqtt_server =" 192.168.133.68"; 
// const char* mqtt_user = "TranNhung"; 
// const char* mqtt_pass = "B21DCCN579";       
// const int mqtt_port = 1884;

// // Chủ đề MQTT
// const char* topic_light = "trannhung/esp8266/light";
// const char* topic_fan = "trannhung/esp8266/fan";
// const char* topic_conditioner = "trannhung/esp8266/conditioner";
// const char* topic_all="trannhung/esp8266/all";
// const char* topic_light_status = "trannhung/esp8266/light/status";
// const char* topic_fan_status = "trannhung/esp8266/fan/status";
// const char* topic_conditioner_status = "trannhung/esp8266/conditioner/status";
// const char* topic_all_status="trannhung/esp8266/all/status";
// const char* topic_sensor_data = "trannhung/esp8266/sensor_data";

// // Tạo đối tượng DHT và PubSubClient
// DHT dht(DHTPIN, DHTTYPE);
// WiFiClient espClient; // Sử dụng WiFiClient thay vì WiFiClientSecure
// PubSubClient client(espClient);
// WiFiUDP ntpUDP;
// NTPClient timeClient(ntpUDP, "pool.ntp.org", 7*3600, 60000);

// // Hàm kết nối WiFi
// void setup_wifi() {
//   delay(10);
//   Serial.println();
//   Serial.print("Connecting to ");
//   Serial.println(ssid);

//   WiFi.begin(ssid, password);

//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//   }

//   Serial.println("");
//   Serial.println("WiFi connected");
//   Serial.println("IP address: ");
//   Serial.println(WiFi.localIP());
// }

// // Hàm callback xử lý khi nhận tin nhắn từ MQTT
// void callback(char* topic, byte* payload, unsigned int length) {
//   Serial.println("Callback function called");
//   Serial.print("Message arrived [");
//   Serial.print(topic);
//   Serial.print("] ");
//   for (int i = 0; i < length; i++) {
//     Serial.print((char)payload[i]);
//   }
//   Serial.println();

//   // Chuyển payload thành chuỗi để so sánh
//   String message = "";
//   for (int i = 0; i < length; i++) {
//     message += (char)payload[i];
//   }

//   // Xử lý bật/tắt LED dựa trên tin nhắn nhận được
//   String ledState = (message == "on") ? "on" : "off";

//   // Tạo một đối tượng JSON để gửi trạng thái
//   StaticJsonDocument<200> doc;
//   doc["state"] = ledState;

//   char jsonBuffer[512];
//   serializeJson(doc, jsonBuffer);

//   if (strcmp(topic, topic_light) == 0) {
//     Serial.print("Light: "); 
//     digitalWrite(LED1, (ledState == "on") ? HIGH : LOW);
//     client.publish(topic_light_status, jsonBuffer);
//   } else if (strcmp(topic, topic_fan) == 0) {
//     Serial.print("Fan: "); 
//     digitalWrite(LED2, (ledState == "on") ? HIGH : LOW);
//     client.publish(topic_fan_status, jsonBuffer);
//   } else if (strcmp(topic, topic_conditioner) == 0) {
//     Serial.print("Conditioner: "); 
//     digitalWrite(LED3, (ledState == "on") ? HIGH : LOW);
//     client.publish(topic_conditioner_status, jsonBuffer);
//   }
//   // Điều khiển cả 3 đèn cùng lúc
//   else if (strcmp(topic, topic_all) == 0) {
//     Serial.print("All:  "); 
//     digitalWrite(LED1, (ledState == "on") ? HIGH : LOW);
//     digitalWrite(LED2, (ledState == "on") ? HIGH : LOW);
//     digitalWrite(LED3, (ledState == "on") ? HIGH : LOW);
//     client.publish(topic_all_status, jsonBuffer);
//   }
//   Serial.println(ledState);

// }

// // Hàm kết nối lại nếu mất kết nối với MQTT Broker
// void reconnect() {
//   while (!client.connected()) {
//     Serial.print("Attempting MQTT connection...");
//     String clientID =  "ESPClient-";
//     clientID += String(random(0xffff), HEX);
//     if (client.connect(clientID.c_str(), mqtt_user, mqtt_pass)) {
//       Serial.println("connected");
//       client.subscribe(topic_light);
//       client.subscribe(topic_fan);
//       client.subscribe(topic_conditioner);
//       client.subscribe(topic_all);
//     } else {
//       Serial.print("failed, rc=");
//       Serial.print(client.state());
//       Serial.println(" try again in 5 seconds");
//       delay(5000);
//     }
//   }
// }

// void setup() {
//   Serial.begin(115200);
//   pinMode(LED1, OUTPUT);
//   pinMode(LED2, OUTPUT);
//   pinMode(LED3, OUTPUT);
//   pinMode(LDR_PIN, INPUT);

//   setup_wifi();
//   client.setServer(mqtt_server, mqtt_port);
//   client.setCallback(callback);
//   dht.begin();
//   timeClient.begin();  // Bắt đầu NTP client
// }


// void loop() {
//     if (!client.connected()) {
//         reconnect();
//     }
//     client.loop();

//     // Đọc dữ liệu từ DHT11
//     float h = dht.readHumidity();
//     float t = dht.readTemperature(); // Nhiệt độ theo Celsius

//     // Kiểm tra nếu không đọc được từ DHT11
//     if (isnan(h) || isnan(t)) {
//         Serial.println("Failed to read from DHT sensor!");
//         return; // Nếu không đọc được, dừng hàm loop
//     }

//     // Đọc giá trị từ quang trở
//     int ldrValue = analogRead(LDR_PIN);
    
//     // Tính toán Lux từ giá trị đọc được từ quang trở
//     float lux = (float)ldrValue * (3.3 / 1024.0) * 1000; // Giả định điện áp tối đa là 3.3V và giá trị ADC 10-bit

//     // Cập nhật thời gian từ NTP
//     timeClient.update();
//     unsigned long currentTime = timeClient.getEpochTime();
//     struct tm *ptm = gmtime((time_t *)&currentTime);

//     int day = ptm->tm_mday;
//     int month = ptm->tm_mon + 1;  // Tháng bắt đầu từ 0, nên cần +1
//     int year = ptm->tm_year + 1900;  // Năm bắt đầu từ 1900
//     int hour = ptm->tm_hour;
//     int minute = ptm->tm_min;
//     int second = ptm->tm_sec;

//     // Xuất nhiệt độ, độ ẩm, Lux và thời gian ra Serial
//     Serial.print("Humidity: ");
//     Serial.print(h);
//     Serial.print(" %\t");
//     Serial.print("Temperature: ");
//     Serial.print(t);
//     Serial.print(" *C\t");
//     Serial.print("Lux: ");
//     Serial.println(lux);
    
//     // In thời gian cụ thể
//     Serial.printf("Date/Time: %02d-%02d-%04d %02d:%02d:%02d\n", day, month, year, hour, minute, second);

//     // Tạo chuỗi JSON
//     StaticJsonDocument<200> doc;
//     doc["temperature"] = t;
//     doc["humidity"] = h;
//     doc["lux"] = lux;
//     // Định dạng ngày giờ theo kiểu dd-mm-yyyy hh:mm:ss
//     String dateTimeString = String(ptm->tm_mday) + "-" + 
//                       String(ptm->tm_mon + 1) + "-" + 
//                       String(ptm->tm_year + 1900) + " " + 
//                       String(ptm->tm_hour) + ":" + 
//                       String(ptm->tm_min) + ":" + 
//                       String(ptm->tm_sec);

//     // Thêm zero-padding cho các giá trị dưới 10 (giờ, phút, giây)
//     String formattedHour = (ptm->tm_hour < 10 ? "0" : "") + String(ptm->tm_hour);
//     String formattedMinute = (ptm->tm_min < 10 ? "0" : "") + String(ptm->tm_min);
//     String formattedSecond = (ptm->tm_sec < 10 ? "0" : "") + String(ptm->tm_sec);

//     // Kết hợp lại thành chuỗi thời gian hoàn chỉnh
//     dateTimeString = String(ptm->tm_mday) + "-" + 
//                  String(ptm->tm_mon + 1) + "-" + 
//                  String(ptm->tm_year + 1900) + " " + 
//                  formattedHour + ":" + 
//                  formattedMinute + ":" + 
//                  formattedSecond;

//     // Gán vào đối tượng JSON
//     doc["Date/Time"] = dateTimeString; 

//     char jsonBuffer[512];
//     serializeJson(doc, jsonBuffer);

//     // Gửi chuỗi JSON qua MQTT
//     client.publish(topic_sensor_data, jsonBuffer);

//     delay(2000); // Đợi 2 giây trước khi lặp lại
// }
