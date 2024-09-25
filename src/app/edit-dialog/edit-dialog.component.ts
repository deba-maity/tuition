import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-edit-dialog',
  templateUrl: './edit-dialog.component.html',
  styleUrls: ['./edit-dialog.component.css'],
})
export class EditDialogComponent {
  editedItem: any;

  constructor(
    public dialogRef: MatDialogRef<EditDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    // Initialize the editedItem with the data passed from the table component
    this.editedItem = { ...data };
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }
}
