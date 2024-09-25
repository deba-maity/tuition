import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DataEntryComponent } from './data-entry/data-entry.component';
import { DataListComponent } from './data-list/data-list.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { TableComponent } from './table/table.component';
import { EditComponent } from './edit/edit.component';
import { DataService } from './data.service';
import { EditDialogComponent } from './edit-dialog/edit-dialog.component';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { PasswordGuard } from './password.guard';
import { EditGuard } from './edit.guard';
@NgModule({
  declarations: [
    AppComponent,
    DataEntryComponent,
    DataListComponent,
    TableComponent,
    EditComponent,
    EditDialogComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    MatDatepickerModule,
    MatNativeDateModule,
    BrowserAnimationsModule,
    MatIconModule,
    MatSelectModule,
  ],
  providers: [DataService, PasswordGuard, EditGuard],
  bootstrap: [AppComponent],
})
export class AppModule {}
