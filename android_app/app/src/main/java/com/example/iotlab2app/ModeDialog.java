package com.example.iotlab2app;


import android.app.AlertDialog;
import android.app.Dialog;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatDialogFragment;

public class ModeDialog extends AppCompatDialogFragment {
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState){
        AlertDialog.Builder builder=new AlertDialog.Builder(getActivity());
        builder.setTitle("Information")
                .setCancelable(false)
                .setMessage("Waiting for response from server, the Light Status will update if succeed.");
        return builder.create();
    }
}
