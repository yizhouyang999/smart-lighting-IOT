package com.example.iotlab2app;


import android.os.AsyncTask;

import android.os.Bundle;
import java.sql.*;


class Async extends AsyncTask<Void, Void, Void> {



    String records = "",error="";

    @Override
    protected Void doInBackground(Void... voids) {

        try

        {

            Class.forName("com.mysql.jdbc.Driver");

            Connection connection = DriverManager.getConnection("jdbc:mysql://192.168.1.2:3306/python", "yang", "123456");

            Statement statement = connection.createStatement();

            ResultSet resultSet = statement.executeQuery("SELECT * FROM iot_users");

            while(resultSet.next()) {

                records += resultSet.getString(1) + " " + resultSet.getString(2) + "\n";

            }

        }

        catch(Exception e)

        {

            error = e.toString();

        }

        return null;

    }



    @Override

    protected void onPostExecute(Void aVoid) {

//        text.setText(records);
//
//        if(error != "")
//
//            errorText.setText(error);
//
//        super.onPostExecute(aVoid);

    }





}
