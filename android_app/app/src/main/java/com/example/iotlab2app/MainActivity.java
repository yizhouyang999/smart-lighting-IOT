package com.example.iotlab2app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.io.BufferedReader;
import java.io.Console;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.concurrent.TimeUnit;

import ch.ethz.ssh2.Connection;
import ch.ethz.ssh2.Session;
import ch.ethz.ssh2.StreamGobbler;

public class MainActivity extends AppCompatActivity {
    String x = "";
    TextView txv_temp_indoor = null;
    Switch lightToggle = null;
    Button btnUpdateTemp = null;
    Switch lightMode = null;

    String current_mode="";
    Boolean first_time=true;
    ModeDialog modeDialog=new ModeDialog();

    /**
     * variables for Mqtt
     */
    private MqttAndroidClient client;
    private static final String SERVER_URI = "tcp://test.mosquitto.org:1883";
    private static final String TAG = "MainActivity";

    /**
     * subscribe in the client
     *
     * @param topicToSubscribe
     */
    private void subscribe(String topicToSubscribe) {
        final String topic = topicToSubscribe;
        int qos = 1;
        try {
            IMqttToken subToken = client.subscribe(topic, qos);
            subToken.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    System.out.println("Subscription successful to topic: " + topic);
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken,
                                      Throwable exception) {
                    System.out.println("Failed to subscribe to topic: " + topic);
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    /**
     * connect to the set broker
     */
    private void connect() {
        String clientId = MqttClient.generateClientId();
        client =
                new MqttAndroidClient(this.getApplicationContext(), SERVER_URI,
                        clientId);
        try {
            IMqttToken token = client.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    // We are connected
                    Log.d(TAG, "onSuccess");
                    System.out.println(TAG + " Success. Connected to " + SERVER_URI);
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Log.d(TAG, "onFailure");
                    System.out.println(TAG + " Oh no! Failed to connect to " +
                            SERVER_URI);
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }


    /**
     * Connect to raspberry pi
     *
     * @param command
     */
    public void run(String command) {
        StrictMode.ThreadPolicy policy = new
                StrictMode.ThreadPolicy.Builder()
                .permitAll().build();
        StrictMode.setThreadPolicy(policy);
        String hostname = "130.237.177.207";
        String username = "pi";
        String password = "IoT@2021";

        try {
            Connection conn = new Connection(hostname);
            conn.connect();
            boolean isAuthenticated = conn.authenticateWithPassword(username,
                    password);
            if (isAuthenticated == false)
                throw new IOException("Authentication failed.");
            Session sess = conn.openSession();
            sess.execCommand(command);
            InputStream stdout = new StreamGobbler(sess.getStdout());
            BufferedReader br = new BufferedReader(new InputStreamReader(stdout));
            x = "";
            while (true) {
                String line = br.readLine();
                if (line == null)
                    break;
                x += line;
                System.out.println(x);
            }
            System.out.println("ExitCode: " + sess.getExitStatus());
            sess.close();
            conn.close();
        } catch (IOException e) {
            e.printStackTrace(System.err);
        }
    }


    /**
     * main method
     *
     * @param savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        txv_temp_indoor = (TextView) findViewById(R.id.indoorTempShow);
        lightToggle = (Switch) findViewById(R.id.btnToggle);
        lightMode = (Switch) findViewById(R.id.smartLightButton);
        btnUpdateTemp = (Button) findViewById(R.id.btnUpdateTemp);

        /**
         * Connect and get from Mqtt broker
         */
        connect();
        client.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {
                if (reconnect) {
                    System.out.println("Reconnected to : " + serverURI);
                    // Re-subscribe as we lost it due to new session
                    subscribe("iot_project");
                } else {
                    System.out.println("Connected to: " + serverURI);
                    subscribe("iot_project");
                }
            }
            @Override
            public void connectionLost(Throwable cause) {
                System.out.println("The Connection was lost.");
            }
            @Override
            public void messageArrived(String topic, MqttMessage message) throws
                    Exception {
                String newMessage = new String(message.getPayload());
                System.out.println(newMessage);
                if(current_mode.equals(newMessage)){
                    modeDialog.dismiss();
                }
                setModeFromMqtt(newMessage);

            }
            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {
            }
        });

        /**
         * Listen to the light switch
         */
        lightToggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    lightMode.setChecked(true);
                } else {
                    if (!lightMode.isChecked()) {
                        new AsyncTask<Integer, Void, Void>(){
                            @Override
                            protected Void doInBackground(Integer... params) {
                                // Add code to fetch data via SSH
                                run("python3 Documents/mode.py off");
                                return null;
                            }
                        }.execute(1);
                        txv_temp_indoor.setText("off");
                        current_mode="off";
                        if(!first_time){
                            modeDialog.show(getSupportFragmentManager(),"dialog");
                        }
                    } else {
                        lightMode.setChecked(false);
                    }
                }
            }
        });


        /**
         * Listen to the mode switch
         */
        lightMode.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    if (!lightToggle.isChecked()) {
                        lightMode.setChecked(false);
                        showToastFailed();
                    } else {
                        new AsyncTask<Integer, Void, Void>(){
                            @Override
                            protected Void doInBackground(Integer... params) {
                                // Add code to fetch data via SSH
                                run("python3 Documents/mode.py auto");
                                return null;
                            }
                        }.execute(1);
                        txv_temp_indoor.setText("auto");
                        current_mode="auto";
                        if(!first_time){
                            modeDialog.show(getSupportFragmentManager(),"dialog");
                        }
                    }
                } else {
                    if (!lightToggle.isChecked()) {
                        new AsyncTask<Integer, Void, Void>(){
                            @Override
                            protected Void doInBackground(Integer... params) {
                                // Add code to fetch data via SSH
                                run("python3 Documents/mode.py off");
                                return null;
                            }
                        }.execute(1);
                        txv_temp_indoor.setText("off");
                        current_mode="off";
                        if(!first_time){
                            modeDialog.show(getSupportFragmentManager(),"dialog");
                        }
                    } else {
                        new AsyncTask<Integer, Void, Void>(){
                            @Override
                            protected Void doInBackground(Integer... params) {
                                // Add code to fetch data via SSH
                                run("python3 Documents/mode.py on");
                                return null;
                            }
                        }.execute(1);
                        txv_temp_indoor.setText("on");
                        current_mode="on";
                        if(!first_time){
                            modeDialog.show(getSupportFragmentManager(),"dialog");
                        }
                    }

                }
            }
        });

        /**
         * Listen to the button
         */
        btnUpdateTemp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Add code
                openLoginActivity();


            }
        });

//        /**
//         * Listen to the button
//         */
//        btnUpdateTemp.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                // Add code
//                new AsyncTask<Integer, Void, Void>() {
//                    @Override
//                    protected Void doInBackground(Integer... params) {
//                        // Add code to fetch data via SSH
//
//                        return null;
//                    }
//
//                    @Override
//                    protected void onPostExecute(Void v) {
//
//
//                    }
//
//                }.execute(1);
//            }
//        });

    }


    /**
     * the function show toast when user try to turn on auto without turon on light
     */
    public void showToastFailed(){
        LayoutInflater inflater=getLayoutInflater();
        View layout=inflater.inflate(R.layout.mode_fail,(ViewGroup) findViewById(R.id.mode_fail_root));
        Toast toast=new Toast(getApplicationContext());
        toast.setGravity(Gravity.BOTTOM,0,400);
        toast.setDuration(Toast.LENGTH_SHORT);
        toast.setView(layout);

        toast.show();
    }


    /**
     * this function logout the user
     */
    public void openLoginActivity() {
        Intent intent = new Intent(this, LoginActivity.class);
        startActivity(intent);
    }


    /**
     * this function change mode according to the mqtt response
     * @param mode
     */
    public void setModeFromMqtt(String mode){
        if(!first_time){
            return;
        }
        if(mode.equals("auto")){
            lightToggle.setChecked(true);
            lightMode.setChecked(true);
        }
        else if(mode.equals("off")){
            lightToggle.setChecked(false);
            lightMode.setChecked(false);
        }
        else if(mode.equals("on")){
            lightToggle.setChecked(true);
            lightMode.setChecked(false);
        }
        first_time=false;
    }


}