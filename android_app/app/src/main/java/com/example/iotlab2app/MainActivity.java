package com.example.iotlab2app;

import androidx.appcompat.app.AppCompatActivity;

import android.os.AsyncTask;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.Console;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import ch.ethz.ssh2.Connection;
import ch.ethz.ssh2.Session;
import ch.ethz.ssh2.StreamGobbler;

public class MainActivity extends AppCompatActivity {
    String x = "";

    public void run (String command) {
        StrictMode.ThreadPolicy policy = new
                StrictMode.ThreadPolicy.Builder()
                .permitAll().build();
        StrictMode.setThreadPolicy(policy);
        String hostname = "130.237.177.205";
        String username = "pi";
        String password = "IoT@2021";

        try
        {
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
            while (true){
                String line = br.readLine();
                if (line == null)
                    break;
                x+=line;
                System.out.println(x);
            }
            System.out.println("ExitCode: " + sess.getExitStatus());
            sess.close();
            conn.close();
        }
        catch (IOException e)
        { e.printStackTrace(System.err);
        }
    }

    TextView txv_temp_indoor = null;
    Switch lightToggle = null;
    Button btnUpdateTemp = null;
    Switch lightMode=null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        txv_temp_indoor = (TextView) findViewById(R.id.indoorTempShow);


        lightToggle = (Switch) findViewById(R.id.btnToggle);
        lightMode=(Switch) findViewById(R.id.smartLightButton) ;
        lightToggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked){
                    lightMode.setChecked(true);
                }
                else{
                    if(!lightMode.isChecked()){
//                        new AsyncTask<Integer, Void, Void>(){
//                            @Override
//                            protected Void doInBackground(Integer... params) {
//                                // Add code to fetch data via SSH
//                                run("python mode.py off");
//                                return null;
//                            }
//                        }.execute(1);
                        txv_temp_indoor.setText("turn off");
                    }
                    else{
                        lightMode.setChecked(false);
                    }
                }
            }
        });
        lightMode.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked){
                    if(!lightToggle.isChecked()){
                        lightMode.setChecked(false);
                    }
                    else{
//                        new AsyncTask<Integer, Void, Void>(){
//                            @Override
//                            protected Void doInBackground(Integer... params) {
//                                // Add code to fetch data via SSH
//                                run("python mode.py auto");
//                                return null;
//                            }
//                        }.execute(1);
                        txv_temp_indoor.setText("auto");
                    }
                }
                else{
                    if(!lightToggle.isChecked()){
//                        new AsyncTask<Integer, Void, Void>(){
//                            @Override
//                            protected Void doInBackground(Integer... params) {
//                                // Add code to fetch data via SSH
//                                run("python mode.py off");
//                                return null;
//                            }
//                        }.execute(1);
                        txv_temp_indoor.setText("turn off");
                    }
                    else{
//                        new AsyncTask<Integer, Void, Void>(){
//                            @Override
//                            protected Void doInBackground(Integer... params) {
//                                // Add code to fetch data via SSH
//                                run("python mode.py on");
//                                return null;
//                            }
//                        }.execute(1);
                        txv_temp_indoor.setText("static");
                    }

                }
            }
        });


        btnUpdateTemp = (Button) findViewById(R.id.btnUpdateTemp);
        btnUpdateTemp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Add code
                new AsyncTask<Integer, Void, Void>(){
                    @Override
                    protected Void doInBackground(Integer... params) {
                        // Add code to fetch data via SSH

                        return null;
                    }
                    @Override
                    protected void onPostExecute(Void v) {


                    }

                }.execute(1);
            }
        });

    }





}