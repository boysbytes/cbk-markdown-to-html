---
title: "A1 Class - Use of capacitive sensing"
description: "Introduction to capacitive sensing and the ESP32-S3 touchRead() function, including how to calibrate a sensor for accurate moisture measurement."
target_audience: "13-17 year old students"
purpose: "lesson"
project: "A"
lesson_id: "A1"
type: "Class"
version: "v1.0"
---

## A1 Class - Use of capacitive sensing

> **Learning objectives**
> - Explain what capacitance is and how the ESP32-S3 uses touch pins to detect changes in capacitance.
> - Describe how soil moisture affects a capacitive sensor reading, and why wet soil produces a lower value than dry soil.
> - Calibrate a capacitive sensor by recording `touchRead()` values for known dry and wet soil conditions.

> ⚠️ **Board compatibility:** This lesson is designed for ESP32-S3 boards (including ESP32-S3-CAM). If you have an ESP32 board, you can still follow the instructions. The code works the same way, but pin locations differ between board types.

In this lesson you will learn about the capacitive sensing pins on the ESP32-S3, and how you can use them to measure physical properties like soil moisture.

### Step 1 - What is capacitance?

1. In electronics, a **capacitor** is like a tiny, electrical sponge. It stores electrical energy. 

    **Capacitance** is the ability to store that charge.

2. The ESP32-S3 has touch-sensitive pins that can detect changes in capacitance. 

    When you touch one, the capacitance of the pin changes, and the ESP32-S3 detects it.

    The touch-sensitive pins on the ESP32-S3 are indicated as T1 to T14.

    <img src="./images/project-b/esp32s3-pinout.png" alt="A diagram showing the pinout of an ESP32-S3 development board, labeling all GPIO pins and their functions." width="560"><br>
    Source: [Freenove® ESP32-S3 WROOM](https://github.com/Freenove/Freenove_ESP32_S3_WROOM_Board)

3. How do we use capacitance to help our plant?

    Soil acts like a part of our capacitor.

    Because water is great at holding an electrical charge,

    - **Dry soil** has a low capacitance (like a dry sponge)
    - **Wet soil** has a high capacitance (like a wet sponge)
 
> 💡 The `touchRead()` function on the ESP32-S3 measures capacitance by seeing how long it takes to "fill up" the electrical sponge. A higher capacitance takes longer, which results in a *lower* reading from the function. So, **Wet Soil = Lower `touchRead()` Value**.

### Step 2 - Reading capacitance

1. Set up this circuit.

    <img src="./images/project-b/schematic-esp32s3-touch.png" alt="Circuit diagram showing a single wire connected to GPIO4 on an ESP32-S3 board, acting as a touch sensor probe." width="400">

2. Create a program that uses the `touchRead()` function and displays the values in the Serial Monitor.

    ```cpp
    void setup() {
        Serial.begin(115200);
        delay(1000); // give time to connect serial monitor
        Serial.println("Touch Sensor Test");
    }

    void loop() {
        // Read the value from the touch sensor
        int touchValue = touchRead(4);

        Serial.print("Touch Value: ");
        Serial.println(touchValue);

        delay(1000);
    }
    ```

3. Upload the program, and then try touching the touch probe (the wire) with your hand.

    Observe the Serial Monitor. You should see the `touchValue` change when you touch the probe.

### Step 3 - The importance of calibration

1. Run the code with the touch probe in these conditions:

    - In the air.
    - In fully dry soil.
    - In fully wet soil.

2. You will notice that the `touchValue` is different for each condition.

3. To make the data useful, you must **calibrate** the sensor. 

    Record the values for "fully dry" and "fully wet".
    
    You will later convert these raw sensor readings into a meaningful percentage (for example, 0% to 100% moisture).

> 🤖 **Want to learn more?** Ask an AI assistant like [Gemini](https://gemini.google.com) or [ChatGPT](https://chat.openai.com):
> ```text
> I'm a 13-17 year old learning about sensor calibration for ESP32-S3. Teach me why calibration is important as my mentor. Rules: Explain ONE idea at a time using real-world examples, ask me a question, then WAIT for my answer. Repeat. Start by asking what I think 'raw sensor readings' means.
> ```

### Step 4 - Share and reflect

1. Discuss in class:

    - What is the relationship between soil moisture and the value you get from `touchRead()`?
    - Why is it important to calibrate a sensor before using its data?
    - Can you think of other things you could measure using capacitance?