package com.example.iotlab2app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.material.button.MaterialButton;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        TextView username = (TextView) findViewById(R.id.username);
        TextView password = (TextView) findViewById(R.id.password);

        MaterialButton login_button = (MaterialButton) findViewById(R.id.login_button);
        MaterialButton help_button = (MaterialButton) findViewById(R.id.forget_password_button);

        login_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (username.getText().toString().equals("admin") && password.getText().toString().equals("admin")) {
                    showToastSuccessful();
                    openMainActivity();
                } else {
                    showToastFailed();
                }
            }
        });

        help_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showToastHelp();
            }
        });
    }

    /**
     * show toast when login successfully
     */
    public void showToastSuccessful(){
        LayoutInflater inflater=getLayoutInflater();
        View layout=inflater.inflate(R.layout.toast_successful,(ViewGroup) findViewById(R.id.toast_successful_root));
        Toast toast=new Toast(getApplicationContext());
        toast.setGravity(Gravity.BOTTOM,0,400);
        toast.setDuration(Toast.LENGTH_SHORT);
        toast.setView(layout);

        toast.show();
    }

    /**
     * show toast when login failed
     */
    public void showToastFailed(){
        LayoutInflater inflater=getLayoutInflater();
        View layout=inflater.inflate(R.layout.toast_failed,(ViewGroup) findViewById(R.id.toast_failed_root));
        Toast toast=new Toast(getApplicationContext());
        toast.setGravity(Gravity.BOTTOM,0,400);
        toast.setDuration(Toast.LENGTH_SHORT);
        toast.setView(layout);

        toast.show();
    }


    /**
     * show toast when user need help
     */
    public void showToastHelp(){
        LayoutInflater inflater=getLayoutInflater();
        View layout=inflater.inflate(R.layout.toast_phone,(ViewGroup) findViewById(R.id.toast_phone_root));
        Toast toast=new Toast(getApplicationContext());
        toast.setGravity(Gravity.BOTTOM,0,400);
        toast.setDuration(Toast.LENGTH_SHORT);
        toast.setView(layout);

        toast.show();
    }


    /**
     * open main/control page of light
     */
    public void openMainActivity() {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
    }
}

