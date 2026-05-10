import java.sql.*;
import java.awt.Font;
import javax.swing.*;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.event.*;
import com.toedter.calendar.JDateChooser;

public class BookWindow {
    private JTextField b_id_txt, b_title_txt, b_publisher_txt, b_search_txt;
    private JComboBox<String> b_year_combo;
    private JDateChooser b_borrowdate_chooser, b_duedate_chooser;
    private JTable table;
    private DefaultTableModel model;
    private JComboBox<String> b_combo_status, b_combo_member;

    public JPanel getPanel(Connection conn) {
        JPanel panel = new JPanel();
        panel.setLayout(null);
        panel.setBounds(0, 0, 895, 541);

        JLabel b_window_label = new JLabel("Book Management");
        b_window_label.setFont(new Font("Tahoma", Font.BOLD, 30));
        b_window_label.setHorizontalAlignment(SwingConstants.CENTER);
        b_window_label.setBounds(261, 26, 306, 47);
        panel.add(b_window_label);

        JPanel b_info_panel = new JPanel();
        b_info_panel.setBounds(36, 84, 331, 409);
        b_info_panel.setBorder(new TitledBorder("Information of Book"));
        b_info_panel.setLayout(null);
        panel.add(b_info_panel);

        JLabel b_id_label = new JLabel("Book ID:");
        b_id_label.setFont(new Font("Tahoma", Font.PLAIN, 16));
        b_id_label.setBounds(25, 23, 130, 25);
        b_info_panel.add(b_id_label);
        b_id_txt = new JTextField();
        b_id_txt.setBounds(140, 25, 152, 20);
        b_info_panel.add(b_id_txt);

        JLabel b_title_label = new JLabel("Title:");
        b_title_label.setFont(new Font("Tahoma", Font.PLAIN, 16));
        b_title_label.setBounds(25, 58, 130, 25);
        b_info_panel.add(b_title_label);
        b_title_txt = new JTextField();
        b_title_txt.setBounds(140, 60, 152, 20);
        b_info_panel.add(b_title_txt);

        JLabel b_borrowdate_label = new JLabel("Borrow Date:");
        b_borrowdate_label.setFont(new Font("Tahoma", Font.PLAIN, 16));
        b_borrowdate_label.setBounds(25, 93, 130, 25);
        b_info_panel.add(b_borrowdate_label);
        b_borrowdate_chooser = new JDateChooser();
        b_borrowdate_chooser.setDateFormatString("yyyy-MM-dd");
        b_borrowdate_chooser.setBounds(140, 95, 152, 20);
        b_info_panel.add(b_borrowdate_chooser);

        JLabel b_duedate_label = new JLabel("Due Date:");
        b_duedate_label.setFont(new Font("Tahoma", Font.PLAIN, 16));
        b_duedate_label.setBounds(25, 128, 130, 25);
        b_info_panel.add(b_duedate_label);
        b_duedate_chooser = new JDateChooser();
        b_duedate_chooser.setDateFormatString("yyyy-MM-dd");
        b_duedate_chooser.setBounds(140, 130, 152, 20);
        b_info_panel.add(b_duedate_chooser);

        JLabel b_publisher_label = new JLabel("Publisher:");
        b_publisher_label.setFont(new Font("Tahoma", Font.PLAIN, 16));
        b_publisher_label.setBounds(25, 163, 130, 25);
        b_info_panel.add(b_publisher_label);
        b_publisher_txt = new JTextField();
        b_publisher_txt.setBounds(140, 165, 152, 20);
        b_info_panel.add(b_publisher_txt);

        JLabel b_year_label = new JLabel("Year:");
        b_year_label.setFont(new Font("Tahoma", Font.PLAIN, 16));
        b_year_label.setBounds(25, 198, 130, 25);
        b_info_panel.add(b_year_label);
        b_year_combo = new JComboBox<>();
        for (int i = 1940; i <= 2025; i++) b_year_combo.addItem(String.valueOf(i));
        b_year_combo.setBounds(140, 200, 152, 20);
        b_info_panel.add(b_year_combo);

        JLabel b_status_label = new JLabel("Status:");
        b_status_label.setFont(new Font("Tahoma", Font.PLAIN, 16));
        b_status_label.setBounds(25, 233, 130, 25);
        b_info_panel.add(b_status_label);
        b_combo_status = new JComboBox<>(new String[]{"Available", "Borrowed"});
        b_combo_status.setBounds(140, 235, 152, 25);
        b_info_panel.add(b_combo_status);

        JLabel b_member_label = new JLabel("Member ID:");
        b_member_label.setFont(new Font("Tahoma", Font.PLAIN, 16));
        b_member_label.setBounds(25, 263, 130, 25);
        b_info_panel.add(b_member_label);
        b_combo_member = new JComboBox<>();
        b_combo_member.setBounds(140, 265, 152, 25);
        b_info_panel.add(b_combo_member);

        JButton b_insert_btn = new JButton("Insert");
        b_insert_btn.setBounds(25, 358, 80, 40);
        b_info_panel.add(b_insert_btn);

        JButton b_delete_btn = new JButton("Delete");
        b_delete_btn.setBounds(122, 358, 80, 40);
        b_info_panel.add(b_delete_btn);

        JButton b_update_btn = new JButton("Update");
        b_update_btn.setBounds(212, 358, 80, 40);
        b_info_panel.add(b_update_btn);

        JPanel b_search_panel = new JPanel();
        b_search_panel.setBounds(391, 433, 433, 60);
        b_search_panel.setBorder(new TitledBorder("Search"));
        b_search_panel.setLayout(null);
        panel.add(b_search_panel);

        JLabel b_search_label = new JLabel("Search by ID:");
        b_search_label.setFont(new Font("Tahoma", Font.PLAIN, 16));
        b_search_label.setBounds(10, 20, 120, 25);
        b_search_panel.add(b_search_label);

        b_search_txt = new JTextField();
        b_search_txt.setBounds(130, 22, 180, 25);
        b_search_panel.add(b_search_txt);

        JButton b_search_btn = new JButton("Search");
        b_search_btn.setBounds(343, 11, 80, 40);
        b_search_panel.add(b_search_btn);

        model = new DefaultTableModel(new String[]{"Book ID", "Title", "Borrow Date", "Due Date", "Publisher", "Year", "Status", "Member ID"}, 0);
        table = new JTable(model);
        JScrollPane b_scroll_pane = new JScrollPane(table);
        b_scroll_pane.setBounds(391, 84, 600, 336);
        panel.add(b_scroll_pane);

        table.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent e) {
                int row = table.getSelectedRow();
                if (row >= 0) {
                    b_id_txt.setText(model.getValueAt(row, 0).toString());
                    b_title_txt.setText(model.getValueAt(row, 1).toString());
                    b_borrowdate_chooser.setDate((Date) model.getValueAt(row, 2));
                    b_duedate_chooser.setDate((Date) model.getValueAt(row, 3));
                    b_publisher_txt.setText(model.getValueAt(row, 4).toString());
                    b_year_combo.setSelectedItem(model.getValueAt(row, 5).toString());
                    b_combo_status.setSelectedItem(model.getValueAt(row, 6).toString());
                    b_combo_member.setSelectedItem(model.getValueAt(row, 7) != null ? model.getValueAt(row, 7).toString() : "");
                }
            }
        });

        loadMembersIntoComboBox(conn);
        loadBooksTable(conn);

        b_insert_btn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                insertBook(conn, panel);
            }
        });

        b_delete_btn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                deleteBook(conn, panel);
            }
        });

        b_update_btn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                updateBook(conn, panel);
            }
        });

        b_search_btn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                searchBook(conn, panel);
            }
        });

        JButton refresh = new JButton("Refresh");
        refresh.setBounds(850, 450, 100, 30);
        panel.add(refresh);

        refresh.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                loadBooksTable(conn);
            }
        });

        return panel;
    }

    private void setDateParameter(PreparedStatement ps, int index, JDateChooser chooser) throws SQLException {
        java.util.Date date = chooser.getDate();
        if (date != null) ps.setDate(index, new java.sql.Date(date.getTime()));
        else ps.setNull(index, Types.DATE);
    }

    private void insertBook(Connection conn, JPanel panel) {
        try {
            PreparedStatement ps = conn.prepareStatement("INSERT INTO book (book_id, title, borrow_date, due_date, publisher, year, status, member_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
            ps.setString(1, b_id_txt.getText());
            ps.setString(2, b_title_txt.getText());
            setDateParameter(ps, 3, b_borrowdate_chooser);
            setDateParameter(ps, 4, b_duedate_chooser);
            ps.setString(5, b_publisher_txt.getText());
            ps.setString(6, (String) b_year_combo.getSelectedItem());
            String status = (String) b_combo_status.getSelectedItem();
            ps.setString(7, status);

            Object member = b_combo_member.getSelectedItem();
            String memberStr = member != null ? member.toString().trim() : "";
            if ("Borrowed".equals(status) && memberStr.isEmpty()) {
                JOptionPane.showMessageDialog(panel, "Member ID is required when status is 'Borrowed'");
                return;
            }
            if (memberStr.isEmpty()) ps.setNull(8, Types.INTEGER);
            else ps.setInt(8, Integer.parseInt(memberStr));

            ps.executeUpdate();
            JOptionPane.showMessageDialog(panel, "Book added successfully");
            loadBooksTable(conn);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void updateBook(Connection conn, JPanel panel) {
        try {
            PreparedStatement ps = conn.prepareStatement("UPDATE book SET title=?, borrow_date=?, due_date=?, publisher=?, year=?, status=?, member_id=? WHERE book_id=?");
            ps.setString(1, b_title_txt.getText());
            setDateParameter(ps, 2, b_borrowdate_chooser);
            setDateParameter(ps, 3, b_duedate_chooser);
            ps.setString(4, b_publisher_txt.getText());
            ps.setString(5, (String) b_year_combo.getSelectedItem());
            String status = (String) b_combo_status.getSelectedItem();
            ps.setString(6, status);

            Object member = b_combo_member.getSelectedItem();
            String memberStr = member != null ? member.toString().trim() : "";
            if ("Borrowed".equals(status) && memberStr.isEmpty()) {
                JOptionPane.showMessageDialog(panel, "Member ID is required when status is 'Borrowed'");
                return;
            }
            if (memberStr.isEmpty()) ps.setNull(7, Types.INTEGER);
            else ps.setInt(7, Integer.parseInt(memberStr));

            ps.setString(8, b_id_txt.getText());
            ps.executeUpdate();
            JOptionPane.showMessageDialog(panel, "Book updated successfully");
            loadBooksTable(conn);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void deleteBook(Connection conn, JPanel panel) {
        try {
            PreparedStatement ps = conn.prepareStatement("DELETE FROM book WHERE book_id=?");
            ps.setString(1, b_id_txt.getText().trim());
            ps.executeUpdate();
            JOptionPane.showMessageDialog(panel, "Book deleted successfully");
            loadBooksTable(conn);
        } catch (Exception ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(panel,"Delete failed: " + ex.getMessage());
        }
    }

    private void searchBook(Connection conn, JPanel panel) {
        try {
            String id = b_search_txt.getText();
            if (id.isEmpty()) {
                JOptionPane.showMessageDialog(panel, "Please enter a book ID to search");
                return;
            }
            PreparedStatement ps = conn.prepareStatement("SELECT * FROM book WHERE book_id = ?");
            ps.setString(1, id);
            ResultSet rs = ps.executeQuery();
            model.setRowCount(0);
            while (rs.next()) {
                model.addRow(new Object[]{
                    rs.getString("book_id"),
                    rs.getString("title"),
                    rs.getDate("borrow_date"),
                    rs.getDate("due_date"),
                    rs.getString("publisher"),
                    rs.getString("year"),
                    rs.getString("status"),
                    rs.getString("member_id")
                });
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void loadBooksTable(Connection conn) {
        try {
            model.setRowCount(0);
            PreparedStatement ps = conn.prepareStatement("SELECT * FROM book");
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                model.addRow(new Object[]{
                    rs.getString("book_id"),
                    rs.getString("title"),
                    rs.getDate("borrow_date"),
                    rs.getDate("due_date"),
                    rs.getString("publisher"),
                    rs.getString("year").substring(0, 4),
                    rs.getString("status"),
                    rs.getString("member_id")
                });
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void loadMembersIntoComboBox(Connection conn) {
        try {
            b_combo_member.removeAllItems();
            b_combo_member.addItem("");
            PreparedStatement ps = conn.prepareStatement("SELECT member_id FROM member");
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                b_combo_member.addItem(rs.getString("member_id"));
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}