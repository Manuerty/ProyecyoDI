package com.example.toolbars;

import android.os.Bundle;
import android.view.ContextMenu;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.widget.Toolbar;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class toolBarDeprecated extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_tool_bar_deprecated);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        Toolbar tb = findViewById(R.id.tb2);
        setSupportActionBar(tb);

        TextView tv = findViewById(R.id.tv1);
        registerForContextMenu(tv);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menudef, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {

        int id = item.getItemId();

        if (id == R.id.op1) {
            Toast.makeText(this, "Opcion 1", Toast.LENGTH_SHORT).show();
            return true;
        }
        if (id == R.id.op2) {
            Toast.makeText(this, "Opcion 2", Toast.LENGTH_SHORT).show();
            return true;
        }
        if (id == R.id.op3) {
            Toast.makeText(this, "Opcion 3", Toast.LENGTH_SHORT).show();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onCreateContextMenu(ContextMenu menu, View v, ContextMenu.ContextMenuInfo menuInfo) {

        getMenuInflater().inflate(R.menu.menudef, menu);
        super.onCreateContextMenu(menu, v, menuInfo);
    }

    @Override
    public boolean onContextItemSelected(@NonNull MenuItem item) {

        int id = item.getItemId();

        if (id == R.id.op1) {
            Toast.makeText(this, "Opcion 1", Toast.LENGTH_SHORT).show();
            return true;
        }
        if (id == R.id.op2) {
            Toast.makeText(this, "Opcion 2", Toast.LENGTH_SHORT).show();
            return true;
        }
        if (id == R.id.op3) {
            Toast.makeText(this, "Opcion 3", Toast.LENGTH_SHORT).show();
            return true;
        }
        if (id == R.id.op4) {
            Toast.makeText(this, "Opcion 4", Toast.LENGTH_SHORT).show();
            return true;
        }
        return super.onContextItemSelected(item);
    }
}