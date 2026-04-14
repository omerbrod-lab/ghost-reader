package org.omerbrod.ghostreader;

import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.app.Notification;
import android.os.Bundle;
import java.io.*;
import java.text.SimpleDateFormat;
import java.util.*;
import org.json.*;

public class NotificationService extends NotificationListenerService {

    private static final String WHATSAPP_PKG = "com.whatsapp";
    private static final String DATA_FILE = "/data/data/org.omerbrod.ghostreader/files/messages.json";

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        if (!sbn.getPackageName().equals(WHATSAPP_PKG)) return;

        Notification notification = sbn.getNotification();
        Bundle extras = notification.extras;

        String title = extras.getString(Notification.EXTRA_TITLE, "");
        String text = extras.getString(Notification.EXTRA_TEXT, "");
        String bigText = extras.getString(Notification.EXTRA_BIG_TEXT, "");

        if (!title.contains(":") && text.contains(":")) {
            String groupName = title;
            String[] parts = text.split(":", 2);
            String sender = parts[0].trim();
            String content = parts.length > 1 ? parts[1].trim() : text;

            if (!bigText.isEmpty() && bigText.contains(":")) {
                String[] bigParts = bigText.split(":", 2);
                content = bigParts.length > 1 ? bigParts[1].trim() : bigText;
            }

            if (content.isEmpty()) {
                content = detectMediaType(extras);
            }

            String timeStr = new SimpleDateFormat("HH:mm",
                Locale.getDefault()).format(new Date());

            saveMessage(groupName, sender, content, timeStr);
        }
    }

    private String detectMediaType(Bundle extras) {
        if (extras.containsKey(Notification.EXTRA_PICTURE)) {
            return "📷 תמונה";
        }
        String subText = extras.getString(Notification.EXTRA_SUB_TEXT, "");
        if (subText.contains("audio") || subText.contains("voice")) {
            return "🎵 הודעה קולית";
        }
        if (subText.contains("document") || subText.contains("pdf")) {
            return "📄 מסמך";
        }
        if (subText.contains("video")) {
            return "🎥 וידאו";
        }
        if (subText.contains("gif")) {
            return "🖼️ GIF";
        }
        return "📎 קובץ";
    }

    private void saveMessage(String group, String sender,
                              String text, String time) {
        try {
            JSONObject data = loadData();
            JSONArray messages;
            if (data.has(group)) {
                messages = data.getJSONArray(group);
            } else {
                messages = new JSONArray();
            }
            JSONObject msg = new JSONObject();
            msg.put("sender", sender);
            msg.put("text", text);
            msg.put("time", time);
            msg.put("timestamp", System.currentTimeMillis() / 1000.0);
            msg.put("read", false);
            messages.put(msg);
            data.put(group, messages);
            writeData(data.toString());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private JSONObject loadData() {
        try {
            File f = new File(DATA_FILE);
            if (!f.exists()) return new JSONObject();
            BufferedReader br = new BufferedReader(new FileReader(f));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) sb.append(line);
            br.close();
            return new JSONObject(sb.toString());
        } catch (Exception e) {
            return new JSONObject();
        }
    }

    private void writeData(String json) {
        try {
            File f = new File(DATA_FILE);
            f.getParentFile().mkdirs();
            FileWriter fw = new FileWriter(f);
            fw.write(json);
            fw.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
