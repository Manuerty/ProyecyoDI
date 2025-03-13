package com.example.toolbars;

import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.widget.Toolbar;
import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.MenuProvider;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        Intent intent = new Intent(this, toolBarDeprecated.class);
        startActivity(intent);

        Toolbar tb = findViewById(R.id.tb1);
        setSupportActionBar(tb);

        addMenuProvider(new MenuProvider() {
            @Override
            public void onCreateMenu(@NonNull Menu menu, @NonNull MenuInflater menuInflater) {
                menuInflater.inflate(R.menu.menudef, menu);

            }

            @Override
            public boolean onMenuItemSelected(@NonNull MenuItem menuItem) {

                int id = menuItem.getItemId();
                if (id == R.id.op1) {
                    Toast.makeText(MainActivity.this, "Opcion 1", Toast.LENGTH_SHORT).show();
                    return true;
                }
                if (id == R.id.op2) {
                    Toast.makeText(MainActivity.this, "Opcion 2", Toast.LENGTH_SHORT).show();
                    return true;
                }
                if (id == R.id.op3) {
                    Toast.makeText(MainActivity.this, "Opcion 3", Toast.LENGTH_SHORT).show();
                    return true;
                }
                if (id == R.id.op4) {
                    Toast.makeText(MainActivity.this, "Opcion 4", Toast.LENGTH_SHORT).show();
                    return true;
                }

                return false;
            }


        });



    }


}