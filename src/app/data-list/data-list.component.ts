import { HttpClient } from '@angular/common/http';
import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-data-list',
  templateUrl: './data-list.component.html',
  styleUrls: ['./data-list.component.css']
})
export class DataListComponent implements OnInit {

  users: any;
  employees: any = [];
  languages: any = [];
  displayedColumns: string[] = ['name', 'description', 'gender', 'contact', 'email', 'password', 'country', 'language', 'skills', 'dob'];
  dataSource: any;
  // dataSource = new MatTableDataSource();

  constructor(private http: HttpClient, private formBuilder: FormBuilder, private router: Router) {

  }

  deleteUser(user: any) {
    // Send a DELETE request to your API to delete the user
    this.http.delete(`http://localhost:3000/employees/${user.id}`).subscribe(() => {
      // Reload the employees list after deletion
      this.loadEmployees();
    });
  }

  editUser(user: any) {
    // Navigate to the edit page, passing the user ID or any necessary data
    this.router.navigate(['/edit', user.id]); // Update the route and parameter accordingly
  }

  ngOnInit() {
this.loadEmployees()
  }

  loadEmployees() {
    this.http.get('http://localhost:3000/employees').subscribe((res: any) => {
      this.employees = res;
    });
  }

  /**
   * Navigation for add user
   */
  onSubmit() {
    this.router.navigate(['/data/entry']);
  }

}
