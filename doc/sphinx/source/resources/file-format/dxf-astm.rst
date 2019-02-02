.. include:: /abbreviation.txt

.. _dxf-astm-ressources-page:

======================
 DXF ASTM File Format
======================

* `ASTM D6673-10 Standard Practice for Sewn Products Pattern Data Interchange-Data Format (Withdrawn 2019) <https://www.astm.org/Standards/D6673.htm>`_

ASTM D6673-10 is based on AutoCAD DXF version R13.

.. ASTM files follow the header, layer and entity structure as defined in the Autodesk DXF version R13.

Each ASTM file contains:

* DXF file header, one pattern style per file;
* DXF entities. In DXF terms an entity can be a line, polyline, point, text, etc.;
* Layers to separate DXF information by type and function. Detail information is assigned to one of
  23 pre-defined layers and a variety of DXF entities;
* Style System text that is common to all pieces in the pattern and is placed once;
* Pattern pieces. ASTM uses DXF blocks, which contain graphical and textual information, to define
  a piece. One block per pattern piece;
* Piece System Text that describes each pattern piece and is part of a block;
* Annotation, part of a block, to clarify instructions for production;
* Instructions for further processing for the purpose of grading, nesting, cutting, etc.

ASTM defines 23 layers for the differentiation of information:

 ======= ======================================================= ================================================================
  Layer   Definition                                              Purpose
 ======= ======================================================= ================================================================
  1       Piece boundary                                          Outline of each pattern piece and style system text
  2       Turn points                                             Turn points for layers 1, 8, 11, 14
  3       Curve points                                            Curve points for layers 1, 8, 11, 14
  4       Notches; V-notch and slit-notch; alignment.             Articulation of molding; I-shape or V-shape: alignment pieces
  5       Grade reference and alternate grade reference line(s)   Grading
  6       Mirror line                                             Symmetry of fold
  7       Grain line                                              Direction of fabric grain
  8       Internal line(s)                                        Graphic annotation of placement. Not cut.
  9       Stripe reference line(s)                                Fabric alignment of stripes
  10      Plaid reference line(s)                                 Fabric alignment of chequers
  11      Internal cutouts(s)                                     Cutline inside of outline
  12      Intentionally left blank
  13      Drill holes                                             Punch markers
  14      Sew line(s)                                             Line(s) indicate where to stitch
  15      Annotation text                                         Annotation, not style system text (1) or piece system text (1)
  80      T-notch                                                 T-shape: slit with T-branch at end of notch
  81      Castle notch                                            U-shape: equal width, rectangular at end of notch
  82      Check notch                                             V-pointed notch, left or right side perpendicular to boundary
  83      U-notch                                                 U-shape: equal width, semi-circle at end of notch
  84      Piece boundary quality validation curves                ASTM: Mandatory system information for polyline(s) layer 1
  85      Internal lines quality validation curves                ASTM: Mandatory system information for polyline(s) layer 8
  86      Internal cutouts quality validation curves              ASTM: Mandatory system information for polyline(s) layer 11
  87      Sew lines quality validation curves                     ASTM: Mandatory system information for polyline(s) layer 14
 ======= ======================================================= ================================================================

Notes:

  * Layer 0 is not in use.
  * Layers must be numbered, not named textually.

ASTM recognizes points for the purpose of:

 ============== ======= ================================================================================================
  Point          Layer   Function
 ============== ======= ================================================================================================
  Turn points    2       Turn points for piece boundary (1), internal lines (8), internal cutouts (11), sew lines (14)
  Curve points   3       Curve points for piece boundary (1), internal lines (8), internal cutouts (11), sew lines (14)
  Notches        4       Slit and V-notches definition
  Grading        5       Grade reference location
  Stripes        9       Stripe match points for alignment (optional)
  Plaids         10      Plaid match points for alignment (optional)
  Drill holes    13      Punch marker location and definition
  T-notch        80      T-notch definition
  Castle-notch   81      Castle-notch definition
  Check-notch    82      Check-notch definition
  U-notch        83      U-notch definition
 ============== ======= ================================================================================================

ASTM uses the DXF block structure to group all elements of a pattern piece.
