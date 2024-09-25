import { Component } from '@angular/core';
// import { MatDialog } from '@angular/material/dialog';
import { EditDialogComponent } from '../edit-dialog/edit-dialog.component';
import { Router } from '@angular/router';
@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.css'],
})
export class TableComponent {

  password: string = '';
  constructor(private router: Router) {}

  login(password: string) {
    if (password === 'maity@29') {
      // Navigate to the route where actions are enabled
      this.router.navigate(['/data-list']);
    } else {
      alert('Incorrect password. Try again.');
    }
  }

}
